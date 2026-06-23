package sagc.authz

import input.attributes.request.http as http_request

# ==========================================
# 🛑 DEFAULT POSTURE: FAIL-CLOSED
# ==========================================
default allow = false

# ==========================================
# ✅ AUTHORIZATION LOGIC
# ==========================================
allow if {
    is_post_request
    is_llm_endpoint
    has_valid_agent_id
    budget_sufficient
}

is_post_request if {
    http_request.method == "POST"
}

is_llm_endpoint if {
    startswith(http_request.path, "/v1/chat/completions")
}

has_valid_agent_id if {
    http_request.headers["x-internal-agent-id"] != ""
}

budget_sufficient if {
    agent_id := http_request.headers["x-internal-agent-id"]
    current_balance := data.budgets[agent_id].remaining_tokens
    current_balance > 0
}

# ==========================================
# 🛑 UNIVERSAL DENIAL HANDLER
# ==========================================
envoy_response := response if {
    not allow
    
    # Logic to determine status and reason
    reason := denial_reason
    status := denial_status

    response := {
        "allowed": false,
        "http_status": status,
        "body": sprintf("{\"error\": \"SAGC Guardrail Triggered: %s\", \"enforcement\": \"opa-sidecar\"}", [reason]),
        "headers": {
            "Content-Type": "application/json",
            "x-sagc-enforcement": "opa-sidecar"
        }
    }
}

denial_reason := "INSUFFICIENT_FUNDS" if {
    not budget_sufficient
} else := "UNAUTHORIZED"

denial_status := 402 if {
    not budget_sufficient
} else := 403