from fastapi import FastAPI, Request
from datetime import datetime
import redis
import json
import sys
import os
import time
from security import validate_fencing_token

# Configuration
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, socket_connect_timeout=3)

# --- SAGC Principal-Level Fiscal Logic ---

LUA_DEDUCTION_SCRIPT = """
local budget_key = KEYS[1]
local cost = tonumber(ARGV[1])
local agent_id = ARGV[2]
local current = tonumber(redis.call('GET', budget_key) or 0)

if current >= cost then
    redis.call('DECRBY', budget_key, cost)
    return 1
else
    return 0
end
"""

class RedisRateLimiter:
    """Distributed Sliding Window Rate Limiter for Audit Logs"""
    def __init__(self, client, max_events: int, window_seconds: int):
        self.client = client
        self.max_events = max_events
        self.window_seconds = window_seconds
    
    def is_allowed(self, agent_id: str) -> bool:
        key = f"audit_rate_limit:{agent_id}"
        now = time.time()
        window_start = now - self.window_seconds
        
        try:
            # Execute atomic pipeline for sliding window
            pipe = self.client.pipeline()
            pipe.zremrangebyscore(key, 0, window_start) # Remove old events
            pipe.zcard(key)                             # Count events in window
            pipe.zadd(key, {str(now): now})             # Add current event
            pipe.expire(key, self.window_seconds + 10)  # Cleanup key later
            results = pipe.execute()
            
            event_count = results[1]
            return event_count < self.max_events
        except Exception:
            # Fail-Closed: If Redis is down, we drop logs to prevent unmonitored spam
            return False

# Enforce 100 events per 60 seconds per agent
audit_rate_limiter = RedisRateLimiter(redis_client, max_events=100, window_seconds=60)

def emit_audit_event(event_type, status, agent_id, details):
    if not audit_rate_limiter.is_allowed(agent_id):
        return  # Drop spam to protect the audit sink
        
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "status": status,
        "agent_id": agent_id,
        "details": details
    }
    sys.stdout.write(json.dumps(log_entry) + "\n")
    sys.stdout.flush()

def check_budget(agent_id, cost):
    try:
        result = redis_client.eval(LUA_DEDUCTION_SCRIPT, 1, f"budget:{agent_id}", cost, agent_id)
        if result == 1:
            return "ALLOW"
        
        emit_audit_event("fiscal", "deny", agent_id, {"reason": "INSUFFICIENT_FUNDS"})
        return "DENY"
        
    except Exception as e:
        emit_audit_event("fiscal", "deny", agent_id, {"reason": "REDIS_OUTAGE", "error": str(e)})
        return "DENY"

def check_budget_with_fencing(agent_id, cost, provided_token):
    try:
        prev_token = redis_client.get(f"{agent_id}:fencing_token_previous")
        prev_token_str = prev_token.decode('utf-8') if prev_token else "genesis"
    except Exception as e:
        emit_audit_event("fiscal", "deny", agent_id, {"reason": "REDIS_OUTAGE", "error": str(e)})
        return "DENY"
        
    if not validate_fencing_token(agent_id, provided_token, prev_token_str):
        emit_audit_event("fiscal", "deny", agent_id, {"reason": "INVALID_FENCING_TOKEN"})
        return "DENY"
        
    return check_budget(agent_id, cost)

app = FastAPI()

@app.post("/v1/chat/completions")
async def handle_request(request: Request):
    agent_id = request.headers.get("x-internal-agent-id", "unknown")
    fencing_token = request.headers.get("x-fencing-token", "")
    cost = 100 # Simulated cost logic
    
    if check_budget_with_fencing(agent_id, cost, fencing_token) == "ALLOW":
        return {"status": "ok"}
    else:
        return {"status": "denied"}, 403
