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