from fastapi import FastAPI, Request
from datetime import datetime
import redis
import json
import sys
import os

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

def emit_audit_event(event_type, status, agent_id, details):
    # (Simplified for now; ensured structured output)
    log_entry = {"timestamp": datetime.utcnow().isoformat(), "event": event_type, "status": status, "agent_id": agent_id, "details": details}
    sys.stdout.write(json.dumps(log_entry) + "\n")

def check_budget(agent_id, cost):
    """
    Principal-level implementation: STRICT Fail-Closed.
    """
    try:
        # Atomic check-and-decrement via Lua
        result = redis_client.eval(LUA_DEDUCTION_SCRIPT, 1, f"budget:{agent_id}", cost, agent_id)
        if result == 1:
            return "ALLOW"
        
        emit_audit_event("fiscal", "deny", agent_id, {"reason": "INSUFFICIENT_FUNDS"})
        return "DENY"
        
    except Exception as e:
        # FAIL-CLOSED: The only production-grade posture for fiscal governance
        emit_audit_event("fiscal", "deny", agent_id, {"reason": "REDIS_OUTAGE", "error": str(e)})
        return "DENY"

app = FastAPI()

@app.post("/v1/chat/completions")
async def handle_request(request: Request):
    agent_id = request.headers.get("x-internal-agent-id", "unknown")
    # For now, simulate cost calculation
    cost = 100 
    
    if check_budget(agent_id, cost) == "ALLOW":
        return {"status": "ok"}
    else:
        return {"status": "denied"}, 403
from security import validate_fencing_token

# Updated pipeline check
def check_budget_with_fencing(agent_id, cost, provided_token):
    # Fetch previous token from Redis
    prev_token = redis_client.get(f"{agent_id}:fencing_token_previous") or "genesis"
    
    if not validate_fencing_token(agent_id, provided_token, prev_token.decode('utf-8')):
        emit_audit_event("fiscal", "deny", agent_id, {"reason": "INVALID_FENCING_TOKEN"})
        return "DENY"
        
    return check_budget(agent_id, cost)
