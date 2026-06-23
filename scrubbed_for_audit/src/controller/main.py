import os
import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Serverless Agentic Governance Controller",
    version="1.0.0"
)

# Configuration derived from the environment
LITELLM_PROXY_URL = os.getenv("LITELLM_PROXY_URL", "http://litellm-service.agentic.svc.cluster.local:4000")

class AgentPayload(BaseModel):
    task_id: str = Field(..., description="Unique tracker for the agent workflow execution")
    prompt: str = Field(..., description="The raw prompt or instruction intended for the LLM")
    fallback_allowed: bool = Field(default=True, description="Enables cascading routing to higher-tier models")

@app.get("/healthz", status_code=status.HTTP_200_OK)
async def health_check():
    """Standard Kubernetes liveness/readiness endpoint."""
    return {"status": "healthy"}

@app.post("/v1/execute", status_code=status.HTTP_200_OK)
async def route_and_execute(payload: AgentPayload):
    """
    Intercepts the agent request, prepares the payload for the LiteLLM gateway,
    and enforces our cascading model routing strategy.
    """
    # Logical model name pointing to our LiteLLM cascade
    target_model = "standard-agent" 

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{LITELLM_PROXY_URL}/v1/chat/completions",
                json={
                    "model": target_model,
                    "messages": [{"role": "user", "content": payload.prompt}]
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Upstream gateway returned error: {response.text}"
                )
                
            return response.json()
            
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unable to reach routing gateway: {exc}"
            )