import os
import logging
from fastapi import HTTPException, Request

logger = logging.getLogger(__name__)

LITELLM_MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "")
BYPASS_AUTH = os.getenv("BYPASS_AUTH", "false").lower() == "true"


async def verify_iap_jwt(request: Request) -> dict:
    """
    Validates Bearer token against LITELLM_MASTER_KEY.
    Function name retained for import compatibility with main.py.
    """
    if BYPASS_AUTH:
        logger.warning("BYPASS_AUTH=true — skipping authentication (dev only)")
        return {}

    if not LITELLM_MASTER_KEY:
        logger.error("LITELLM_MASTER_KEY not configured")
        raise HTTPException(status_code=503, detail="Auth not configured")

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or malformed Authorization header. Expected: Bearer <key>"
        )

    token = auth_header.removeprefix("Bearer ")
    if token != LITELLM_MASTER_KEY:
        logger.warning("Invalid bearer token from %s", request.client.host)
        raise HTTPException(status_code=403, detail="Invalid API key")

    logger.info("Authenticated request from %s", request.client.host)
    return {"authenticated": True, "method": "bearer"}
