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
