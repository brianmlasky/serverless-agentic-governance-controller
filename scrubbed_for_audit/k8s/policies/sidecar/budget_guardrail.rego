package sagc.authz

import rego.v1
import input.attributes.request.http as http_request

# VULN 3 FIX: Explicit defaults for both the boolean and the response payload
default allow := false
default envoy_response := {
    "allowed": false,
    "http_status": 403,
    "body": "{\"error\": \"SAGC Guardrail Triggered: Request denied by default policy. Unauthorized, missing identity, or undefined state.\"}",
    "headers": {
        "Content-Type": "application/json",
        "x-sagc-enforcement": "opa-sidecar"
    }
}

allow if {
    is_post_request
    is_llm_endpoint
    has_valid_agent_identity
    budget_sufficient
}

is_post_request if {
    http_request.method == "POST"
}

is_llm_endpoint if {
    startswith(http_request.path, "/v1/chat/completions")
}

# VULN 2 FIX: Cryptographic Identity Binding
# We extract the SPIFFE identity directly from Envoy's validated mTLS context.
has_valid_agent_identity if {
    spiffe_id := input.attributes.source.principal
    startswith(spiffe_id, "spiffe://sagc.internal/ns/agentic/sa/")
}

# VULN 1 FIX: Atomic execution and safe attribute checking
budget_sufficient if {
    spiffe_id := input.attributes.source.principal

    # We execute a synchronous atomic deduction via an internal service call.
    # We only allow the outbound request if the atomic write succeeds and balance >= 0.
    response := http.send({
        "method": "POST",
        "url": "http://sagc-controller.agentic.svc.cluster.local:8080/v1/budget/decr",
        "body": {"agent_id": spiffe_id, "estimated_tokens": 1000},
        "timeout": "50ms"
    })
    
    response.status_code == 200
    response.body.new_balance >= 0
}

# VULN 3 FIX: Override the default 403 with a 429 ONLY when budget is explicitly exhausted
envoy_response := response if {
    not allow
    not budget_sufficient
    has_valid_agent_identity

    response := {
        "allowed": false,
        "http_status": 429,
        "body": "{\"error\": \"SAGC Guardrail Triggered: Token Burn Rate limit exceeded or Atomic Write Failed. Traffic dropped.\"}",
        "headers": {
            "Content-Type": "application/json",
            "x-sagc-enforcement": "opa-sidecar"
        }
    }
}
