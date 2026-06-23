from datetime import datetime
import sys
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
import logging
import json
import time
import asyncio
import os
# NEW: Prometheus imports
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Setup Metrics
registry = CollectorRegistry()
TOKEN_USAGE = Gauge('agentic_token_usage_total', 'Total tokens consumed', registry=registry)
BUDGET_LIMIT = Gauge('agentic_budget_limit', 'Maximum token budget', registry=registry)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("agentic-sre")

async def check_policy_and_budget(request: Request):
    if request.method == "POST":
        body = await request.body()
        data_in = json.loads(body) if body else {}
        tokens_used = data_in.get("tokens", 100)
    else:
        tokens_used = 0

    budget_file = "budget.json"
    with open(budget_file, "r+") as f:
        data = json.load(f)
        if data["current_usage"] + tokens_used > data["max_token_budget"]:
            return False, f"Budget exceeded: {data['current_usage'] + tokens_used} > {data['max_token_budget']}"
        
        data["current_usage"] += tokens_used
        # NEW: Update Prometheus Metrics
        TOKEN_USAGE.set(data["current_usage"])
        BUDGET_LIMIT.set(data["max_token_budget"])
        
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    return True, "Authorized"

@app.middleware("http")
async def enforce_governance(request: Request, call_next):
    is_authorized, reason = await check_policy_and_budget(request)
    if not is_authorized:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": reason})
    response = await call_next(request)
    return response

# NEW: Prometheus scrape endpoint
@app.get("/metrics")
async def get_metrics():
    return Response(content=generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
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

def check_budget(agent_id, cost):
    """
    Principal-level implementation: Fail-Closed.
    If Redis or network is down, we DENY the request to ensure fiscal integrity.
    """
    try:
        # Atomic check-and-decrement via Lua
        result = redis_client.eval(LUA_DEDUCTION_SCRIPT, 1, f"budget:{agent_id}", cost, agent_id)
        return "ALLOW" if result == 1 else "DENY"
    except Exception as e:
        # FAIL-CLOSED: The only production-grade posture for fiscal governance
        emit_audit_event("fiscal", "deny", agent_id, {"reason": "REDIS_OUTAGE", "error": str(e)})
        return "DENY"

# In-memory rate limiter for local log spam prevention
_audit_log_counts = {}

def is_audit_rate_limited(agent_id):
    now = datetime.now().minute
    count = _audit_log_counts.get((agent_id, now), 0)
    if count > 100: # Max 100 events per minute per agent
        return True
    _audit_log_counts[(agent_id, now)] = count + 1
    return False

def emit_audit_event(event_type, status, agent_id, details):
    """
    Standardized log emitter for the SAGC Audit Sink.
    """
    if is_audit_rate_limited(agent_id):
        return
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "fiscal_event" if event_type == "fiscal" else "governance_event",
        "status": status,
        "agent_id": agent_id,
        "details": details,
        "version": "1.0"
    }
    sys.stdout.write(json.dumps(log_entry) + "\n")
    sys.stdout.flush()
