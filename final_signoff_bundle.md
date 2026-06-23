# SAGC Production Certification Bundle

## src/security.py (F1)
```
import hmac
import hashlib
import time
import os
import secrets

# Production secret MUST be injected via K8s Secret
FENCING_SECRET = os.environ.get("SAGC_FENCING_SECRET", "dev-only-change-me")

async def generate_fencing_token_async(agent_id: str, redis_pool) -> str:
    """Generate a token with a server-side nonce commitment to prevent chosen-plaintext attacks."""
    timestamp = str(int(time.time() * 1000))
    nonce = secrets.token_hex(16)
    
    # Store nonce commitment server-side with 5-minute TTL
    redis_key = f"FENCING_NONCE:{agent_id}"
    await redis_pool.setex(redis_key, 300, nonce)
    
    # Generate full 256-bit HMAC signature
    message = f"{agent_id}:{timestamp}:{nonce}".encode()
    signature = hmac.new(FENCING_SECRET.encode(), message, hashlib.sha256).hexdigest()
    
    return f"{agent_id}|{timestamp}|{nonce}|{signature}"

async def validate_fencing_token_async(agent_id: str, provided_token: str, redis_pool) -> bool:
    """Validate token cryptographically and enforce nonce consumption."""
    try:
        parts = provided_token.split('|')
        if len(parts) != 4:
            return False
            
        token_agent_id, token_timestamp, token_nonce, signature = parts
        
        # 1. Identity & Expiry Check (5 minutes)
        if token_agent_id != agent_id:
            return False
        if (int(time.time() * 1000) - int(token_timestamp)) > 300000:
            return False
            
        # 2. Server-side Nonce Check
        redis_key = f"FENCING_NONCE:{agent_id}"
        stored_nonce = await redis_pool.get(redis_key)
        if not stored_nonce or not hmac.compare_digest(token_nonce, stored_nonce):
            return False
            
        # 3. Cryptographic Verification
        message = f"{agent_id}:{token_timestamp}:{token_nonce}".encode()
        expected_signature = hmac.new(FENCING_SECRET.encode(), message, hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            return False
            
        # 4. Consume Nonce (Prevents replay)
        await redis_pool.delete(redis_key)
        return True
        
    except Exception:
        return False

```

## src/main.py (F2 & F3)
```
import asyncio
import time
import json
import sys
import os
import logging
from datetime import datetime  # <-- Add this line
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from redis.asyncio import Redis, ConnectionPool
from contextlib import asynccontextmanager
from security import validate_fencing_token_async

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

# --- LUA SCRIPTS ---
RATE_LIMIT_CHECK_LUA = """
local key = KEYS[1]
local now_ms = tonumber(ARGV[1])
local window_start = tonumber(ARGV[2])
local window_ms = tonumber(ARGV[3])
local max_count = tonumber(ARGV[4])

-- Atomic sliding window + memory leak prevention
redis.call('zremrangebyscore', key, '-inf', window_start)
redis.call('zadd', key, now_ms, tostring(now_ms))
redis.call('expire', key, math.ceil(window_ms / 1000))
local count = redis.call('zcard', key)
return count
"""

LUA_DEDUCTION_SCRIPT = """
local budget_key = KEYS[1]
local cost = tonumber(ARGV[1])
local ttl = tonumber(ARGV[2]) or 2592000  -- 30 days default
local current = tonumber(redis.call('GET', budget_key) or 0)

if current >= cost then
    redis.call('DECRBY', budget_key, cost)
    redis.call('expire', budget_key, ttl)  -- <-- Memory leak prevented
    return 1
else
    return 0
end
"""

class CircuitBreaker:
    """Prevents asynchronous worker starvation during Redis brownouts."""
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0
        self.state = "CLOSED"
    
    async def call(self, coro, timeout=3.0):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker OPEN: Redis unavailable")
        try:
            result = await asyncio.wait_for(coro, timeout=timeout)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except asyncio.TimeoutError:
            self._record_failure()
            raise Exception("Redis timeout")
        except Exception as e:
            self._record_failure()
            raise e
            
    def _record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

# Global state
redis_pool = None
redis_breaker = CircuitBreaker()
rate_limit_sha = None
deduction_sha = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the connection pool lifecycle and pre-load Lua scripts."""
    global redis_pool, rate_limit_sha, deduction_sha
    pool = ConnectionPool.from_url(REDIS_URL, decode_responses=True, max_connections=50)
    redis_pool = Redis(connection_pool=pool)
    try:
        rate_limit_sha = await redis_pool.script_load(RATE_LIMIT_CHECK_LUA)
        deduction_sha = await redis_pool.script_load(LUA_DEDUCTION_SCRIPT)
        logger.info("Async Redis pool initialized and Lua scripts loaded.")
    except Exception as e:
        logger.error(f"Failed to initialize Redis pool: {e}")
    yield
    await redis_pool.close()

app = FastAPI(lifespan=lifespan)

async def check_audit_rate_limit(agent_id: str) -> bool:
    try:
        now_ms = int(time.time() * 1000)
        window_ms = 60000
        max_audits = 100
        key = f"audit_window:{agent_id}"
        
        # Async execution of the atomic Lua script
        count = await redis_breaker.call(
            redis_pool.evalsha(rate_limit_sha, 1, key, now_ms, now_ms - window_ms, window_ms, max_audits)
        )
        return int(count) <= max_audits
    except Exception as e:
        logger.error(f"Rate limit check failed: {e}")
        return False # Fail-closed

async def emit_audit_event(event_type, status, agent_id, details):
    # Always emit critical fiscal events, rate limit only verbose logs
    log_critical = True if (event_type == "fiscal" or status == "deny") else await check_audit_rate_limit(agent_id)
    
    if log_critical:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "status": status,
            "agent_id": agent_id,
            "details": details,
            "priority": "CRITICAL" if status == "deny" else "INFO"
        }
        sys.stdout.write(json.dumps(log_entry) + "\n")
        sys.stdout.flush()

@app.post("/v1/chat/completions")
async def handle_request(request: Request):
    agent_id = request.headers.get("x-internal-agent-id", "unknown")
    fencing_token = request.headers.get("x-fencing-token", "")
    cost = 100
    
    if not redis_pool:
        return JSONResponse({"status": "denied", "error": "Governance service unavailable"}, status_code=503)
        
    try:
        # 1. Cryptographic Nonce Validation
        is_valid_token = await redis_breaker.call(
            validate_fencing_token_async(agent_id, fencing_token, redis_pool)
        )
        if not is_valid_token:
            await emit_audit_event("fiscal", "deny", agent_id, {"reason": "INVALID_FENCING_TOKEN"})
            return JSONResponse({"status": "denied"}, status_code=403)
            
        # 2. Atomic Budget Deduction
        result = await redis_breaker.call(
            redis_pool.evalsha(deduction_sha, 1, f"budget:{agent_id}", cost, 2592000)
        )
        
        if result == 1:
            await emit_audit_event("fiscal", "allow", agent_id, {"cost": cost})
            return {"status": "ok"}
        else:
            await emit_audit_event("fiscal", "deny", agent_id, {"reason": "INSUFFICIENT_FUNDS"})
            return JSONResponse({"status": "denied"}, status_code=403)
            
    except Exception as e:
        await emit_audit_event("fiscal", "deny", agent_id, {"reason": "REDIS_OUTAGE", "error": str(e)})
        return JSONResponse({"status": "denied"}, status_code=403)

@app.get("/healthz")
async def healthz():
    """Non-blocking liveness probe"""
    if not redis_pool:
        return JSONResponse({"status": "not_ready"}, status_code=503)
    try:
        await asyncio.wait_for(redis_pool.ping(), timeout=2.0)
        return {"status": "ready"}
    except Exception:
        return JSONResponse({"status": "degraded"}, status_code=503)

```

## k8s/security/01-identity-rbac.yaml (F4 Part 1)
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: sagc-controller-sa
  namespace: sagc
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: llm-gateway-sa
  namespace: sagc
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: sagc-strict-isolation
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: sagc-isolation-binding
  namespace: sagc
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: sagc-strict-isolation
subjects:
- kind: ServiceAccount
  name: sagc-controller-sa
  namespace: sagc
- kind: ServiceAccount
  name: llm-gateway-sa
  namespace: sagc\n
```

## k8s/policies/network/enforce-sidecar.yaml (F4 Part 2)
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: enforce-opa-sidecar-routing
  namespace: sagc
spec:
  podSelector:
    matchLabels:
      app: llm-gateway
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - serviceAccountSelector:
        matchLabels:
          name: sagc-controller-sa
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - serviceAccountSelector:
        matchLabels:
          name: sagc-controller-sa
    ports:
    - protocol: TCP
      port: 6379

```

