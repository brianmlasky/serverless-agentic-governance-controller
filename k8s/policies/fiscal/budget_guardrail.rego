package sagc.authz

import input.attributes.request.http as http_request

# ==========================================
# 🛑 DEFAULT POSTURE: FAIL-CLOSED
# ==========================================
# By default, every request is denied unless explicitly allowed.
default allow = false

# ==========================================
# ✅ AUTHORIZATION LOGIC
# ==========================================
allow {
    is_post_request
    is_llm_endpoint
    has_valid_agent_id
    budget_sufficient
}

is_post_request {
    http_request.method == "POST"
}

is_llm_endpoint {
    # Matches OpenAI, Vertex AI, or internal routing endpoints
    startswith(http_request.path, "/v1/chat/completions")
}

has_valid_agent_id {
    http_request.headers["x-internal-agent-id"] != ""
}

# Extracts the agent ID and checks the atomic state data injected into OPA
budget_sufficient {
    agent_id := http_request.headers["x-internal-agent-id"]
    
    # data.budgets is populated dynamically via Kubernetes ConfigMaps or an OPA bundle server
    current_balance := data.budgets[agent_id].remaining_tokens
    
    # The agent must have a positive balance to initiate the inference call
    current_balance > 0
}

# ==========================================
# 💸 THE ENVOY RESPONSE (HTTP 402)
# ==========================================
# If the request is denied specifically because of budget exhaustion, 
# instruct the Envoy proxy to return a 402 Payment Required.
envoy_response = response {
    not allow
    not budget_sufficient
    has_valid_agent_id

    response := {
        "allowed": false,
        "http_status": 402,
        "body": "{\"error\": \"SAGC Guardrail Triggered: Insufficient Token Budget. Traffic dropped at the network layer.\"}",
        "headers": {
            "Content-Type": "application/json",
            "x-sagc-enforcement": "opa-sidecar"
        }
    }
}