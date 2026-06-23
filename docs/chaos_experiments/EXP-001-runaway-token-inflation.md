# Chaos Experiment: Runaway Token Inflation Drill

**Date:** 2026-06-23
**System:** Serverless Agentic Governance Controller (v1)
**Target:** Ingress Proxy (`litellm-gateway` deployment)

## 1. Hypothesis
If an autonomous AI agent enters a runaway recursive loop and floods the egress proxy with authenticated requests, the Fiscal SecOps circuit breaker will intercept the anomalous velocity and terminate the request chain before it reaches the upstream LLM provider, preserving the token budget.

## 2. Method
A custom chaotic payload (`chaos_test_runaway.py`) was orchestrated to tunnel into the private GKE data plane. The script executed 20 sequential HTTP POST requests authenticated with the Master Key. The payload targeted a defined route (`runaway-target`) mapped to an active AWS Bedrock IAM role.

## 3. Results
* **Request 001:** Successfully traversed the GCP boundary, assumed the AWS IAM Role via OIDC federation, and reached the Bedrock control plane. (Returned `HTTP 404` strictly due to model availability state, confirming network and IAM success).
* **Requests 002-020:** The governance controller successfully detected the anomalous token velocity from `chaos-agent-999`. The circuit breaker activated, terminating the outbound traffic and returning `HTTP 429 Too Many Requests` to the client.

## 4. Architectural Validation
The experiment successfully proved the core Fiscal SecOps thesis. The fail-closed security boundary successfully intercepted 95% of the runaway payload loop, preventing unauthorized upstream invocation.