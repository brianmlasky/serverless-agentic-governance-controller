import hmac
import hashlib
import time
import os

# Production secret MUST be injected via K8s Secret
FENCING_SECRET = os.environ.get("SAGC_FENCING_SECRET", "dev-only-change-me")

def generate_fencing_token(agent_id: str, previous_token: str) -> str:
    timestamp = str(int(time.time() * 1000))
    message = f"{agent_id}:{previous_token}:{timestamp}".encode()
    signature = hmac.new(FENCING_SECRET.encode(), message, hashlib.sha256).hexdigest()[:16]
    return f"{agent_id}_{timestamp}_{signature}"

def validate_fencing_token(agent_id: str, provided_token: str, stored_previous_token: str) -> bool:
    try:
        parts = provided_token.split('_')
        if len(parts) < 3: return False
        
        token_agent_id, token_timestamp, signature = parts[0], parts[1], parts[2]
        
        # 1. Identity Check
        if token_agent_id != agent_id: return False
        
        # 2. Expiry Check (5 minutes)
        if (int(time.time() * 1000) - int(token_timestamp)) > 300000: return False
        
        # 3. Signature Verification
        expected_token = generate_fencing_token(agent_id, stored_previous_token)
        return hmac.compare_digest(provided_token, expected_token)
    except Exception:
        return False
