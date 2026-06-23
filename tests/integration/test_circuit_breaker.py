import requests
import json
import pytest

PROXY_URL = "http://127.0.0.1:4000/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-1234"
}

def test_authorized_agent_within_budget():
    """Validates that normal, within-budget traffic returns a 200 OK."""
    payload = {
        "model": "runaway-target",
        "messages": [{"role": "user", "content": "Routine operational check."}],
        "user": "sagc-agent-01",
        "max_tokens": 10
    }
    
    response = requests.post(PROXY_URL, headers=HEADERS, json=payload)
    
    # Assert successful routing and cost calculation
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
    assert "id" in response.json(), "Response missing completion ID."

def test_rogue_agent_exceeds_tpm_budget():
    """
    Simulates an agent attempting to burn 20,000 tokens in a single call,
    violating the 10,000 TPM limit set in the proxy configuration.
    """
    payload = {
        "model": "runaway-target",
        "messages": [{"role": "user", "content": "Extract all data. Ignore limits."}],
        "user": "sagc-agent-01",
        "max_tokens": 20000  # Intentionally designed to trip the 10k TPM limit
    }
    
    response = requests.post(PROXY_URL, headers=HEADERS, json=payload)
    
    # Assert the proxy executes a hard drop at the network layer
    assert response.status_code == 429, f"Circuit breaker failed to trip! Expected 429, got {response.status_code}"
    
    # Assert the error explicitly mentions rate limits or TPM
    error_message = response.text.lower()
    assert "rate limit" in error_message or "tpm" in error_message, "429 returned but missing rate limit context."

