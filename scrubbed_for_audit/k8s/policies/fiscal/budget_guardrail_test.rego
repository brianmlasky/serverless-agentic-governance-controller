package test.sagc.authz

# Import the policy we want to test
import data.sagc.authz.envoy_response

# Test: Ensure a POST request with an empty balance is denied with 402
test_insufficient_funds if {
    mock_input := {
        "attributes": {
            "request": {
                "http": {
                    "method": "POST",
                    "path": "/v1/chat/completions",
                    "headers": {"x-internal-agent-id": "empty-budget-agent"}
                }
            }
        }
    }

    mock_data := {
        "budgets": {
            "empty-budget-agent": {"remaining_tokens": 0}
        }
    }

    res := envoy_response with input as mock_input with data as mock_data
    res.http_status == 402
}

# Test: Ensure a non-POST request is denied with 403
test_invalid_method if {
    mock_input := {
        "attributes": {
            "request": {
                "http": {
                    "method": "GET",
                    "path": "/v1/chat/completions",
                    "headers": {"x-internal-agent-id": "funded-agent"}
                }
            }
        }
    }

    res := envoy_response with input as mock_input
    res.http_status == 403
}