# ADR 007: Two-Tiered OPA Governance for Agentic Workloads

## Status
Accepted

## Context & Problem
Autonomous AI agents present two distinct fiscal risks:
1. **Infrastructure Sprawl:** Unlabeled or unauthorized pods scaling up and consuming excessive compute resources (CPU/RAM).
2. **Token Burn:** Legitimate pods executing recursive loops and consuming excessive external LLM tokens ($/token).

A single governance layer cannot effectively mitigate both risks. 

## Decision
Building upon the sidecar proxy interception established in **ADR 001**, we will implement a **Two-Tiered Policy-as-Code Governance Architecture**.

### Tier 1: Cluster Admission (Control Plane)
* **Tool:** Kyverno / OPA Gatekeeper
* **Path:** `k8s/policies/admission/`
* **Mechanism:** Validates Kubernetes manifests during the `Mutating/ValidatingWebhookConfiguration` phase. 
* **Rule:** No pod is allowed to schedule in the `agentic` namespace unless it passes static fiscal checks (e.g., required cost-center labels, requested resource limits).

### Tier 2: Network Authorization (Data Plane)
* **Tool:** OPA Envoy Sidecar
* **Path:** `k8s/policies/sidecar/`
* **Mechanism:** Validates live Layer 7 outbound HTTP traffic.
* **Rule:** Intercepts all egress traffic to LLM endpoints and evaluates atomic budget states. If the token budget is exhausted, it drops the packet and returns an `HTTP 429 Too Many Requests` (preserving local memory state) before the request reaches the public internet.

## Consequences
* **Positive:** Deep defense-in-depth. Infrastructure costs are capped at deployment; token costs are capped at runtime.
* **Positive:** Clear separation of concerns. Platform Engineers manage Tier 1 (Admission); SRE/AppSec manages Tier 2 (Sidecar).
* **Negative:** Increased cognitive load for engineers debugging denied requests (requires checking both Admission logs and Envoy sidecar logs).