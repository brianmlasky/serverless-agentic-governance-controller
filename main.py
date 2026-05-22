from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
import logging
import json
import time
import asyncio
import os

app = FastAPI()

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

if __name__ == "__main__":
    async def mock_call_next(request): return Response(status_code=200)
    async def test():
        # Test Case: POST request with 1500 tokens
        req = Request(scope={"type": "http", "path": "/test", "method": "POST", "headers": []})
        req._body = b'{"tokens": 1500}'
        response = await enforce_governance(req, mock_call_next)
        print(f"Test status: {response.status_code}")
    asyncio.run(test())