# Runbook: FinOps Budget Alert (HTTP 429)

## Symptom
Prometheus alert `FinOpsBudgetExhausted` is firing in #finops-alerts.

## The Context
The SAGC Envoy sidecar is intercepting outbound LLM traffic. It has evaluated a prompt against the OPA policy and determined that the agent's current token balance is <= 0. 

## The "Dollar Saved" Philosophy
This is a "Fail-Closed" event. The agent pod is still running (preserving forensic state), but the network packet was dropped at the egress layer. We are preventing an unconstrained AI loop from burning through the OpEx budget.

## Troubleshooting Path
1. **Verify Policy:** See `k8s/policies/sidecar/budget_guardrail.rego`.
2. **Verify State:** Query the Atomic State Store for the agent's current balance.
3. **Escalation:** Contact FinOps to adjust budget limits via GitOps PR. Never override policy manually.