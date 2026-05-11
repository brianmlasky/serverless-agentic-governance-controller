import os
import httpx
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Agentic Platform API Gateway", version="0.1.0")

# Internal LiteLLM service address (ClusterIP DNS)
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://litellm-gateway.litellm.svc.cluster.local:80")
LITELLM_MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "")

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024

class ChatResponse(BaseModel):
    id: str
    object: str
    model: str
    choices: list

# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok", "service": "api-gateway"}

# ---------------------------------------------------------------------------
# Chat proxy
# ---------------------------------------------------------------------------

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    authorization: Optional[str] = Header(None),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.removeprefix("Bearer ")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{LITELLM_BASE_URL}/v1/chat/completions",
                json=payload.model_dump(),
                headers=headers,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"LiteLLM unreachable: {str(e)}")

    return JSONResponse(content=response.json())
