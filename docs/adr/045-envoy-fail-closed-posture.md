# ADR-045: Envoy Fail-Closed Posture for ext_proc and ext_authz

## Status
Accepted

## Context
An adversarial Red Team audit identified a vulnerability in the Envoy sidecar streaming pipeline. If the out-of-process ML container (Presidio) or OPA policy engine becomes exhausted or crashes due to malicious payload volume, Envoy must decide whether to buffer indefinitely, drop the traffic, or allow it through uninspected (fail-open).

## Decision
All Envoy `ext_authz` and `ext_proc` filters must be explicitly configured with `failure_mode_allow: false`.

## Consequences
- **Positive (Security):** Guarantees that no LLM traffic can egress the cluster without cryptographic authorization and semantic payload inspection. Neutralizes proxy exhaustion bypass attacks.
- **Negative (Availability):** Transitions the architecture to prioritize data security over availability. If the governance sidecars fail, the agentic workload suffers a complete localized network outage.