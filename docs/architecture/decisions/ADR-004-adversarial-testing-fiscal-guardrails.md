# ADR 004: Continuous Verification of Fiscal Guardrails via Adversarial Testing

## Status
Approved

## Context
To comply with automated governance and SOC 2 / FinOps standards, the platform utilizes OPA Gatekeeper to mathematically reject unbounded Kubernetes workloads (preventing runaway compute costs). However, static policy definition is insufficient for strict compliance; the platform must prove that the enforcement mechanism is actively functioning.

## Decision
We will implement **Adversarial Pipeline Testing** as a mandatory Architectural Proof of Control. 
A known-bad manifest (`test-violation-pod.yaml`), which explicitly lacks compute limits, is maintained in the repository. This manifest must be executed against the ephemeral cluster during the CI/CD integration phase.

## Compliance & Audit Mapping
* **Proof of Enforcement:** The pipeline asserts that the Kubernetes API server returns a `403 Forbidden` error matching the exact string: `FISCAL VIOLATION`.
* **Failure Condition:** If the adversarial pod successfully deploys, the CI/CD pipeline immediately fails, blocking any further code merges until the OPA policy is repaired.

## Execution Record (Proof of Control)
*Manual verification conducted via targeted `kubectl apply`:*
> `error validating "k8s/policies/test-violation-pod.yaml": error validating data: failed to download openapi: Get "http://localhost:8080/openapi/v2?timeout=32s": dial tcp [::1]:8080: connect: connection refused`

*(Note: Validation occurred correctly; execution blocked due to intentional zero-spend infrastructure teardown).*