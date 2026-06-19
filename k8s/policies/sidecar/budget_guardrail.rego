package sagc.authz

import rego.v1
import input.attributes.request.http as http_request

default allow := false

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

envoy_response := response if {
    not allow
    not budget_sufficient
    has_valid_agent_id

    response := {
        "allowed": false,
        "http_status": 429,
        "body": "{\"error\": \"SAGC Guardrail Triggered: Token Burn Rate limit exceeded. Traffic dropped at network layer.\"}",
        "headers": {
            "Content-Type": "application/json",
            "x-sagc-enforcement": "opa-sidecar"
        }
    }
}
