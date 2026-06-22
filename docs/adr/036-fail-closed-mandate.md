# ADR 036: Fail-Closed Posture for Governance-Critical Paths

## Status
Accepted

## Context
Previous iterations of the SAGC allowed for "best-effort" performance, inadvertently allowing traffic during Redis outages or timeouts. This is unacceptable for fiscal governance.

## Decision
All governance-critical infrastructure paths (Redis, Audit Sink, Policy Sidecar) must implement strict timeout/circuit-breaker patterns. Any exception (timeout, connection failure, logic error) in the governance path must result in an immediate `DENIED` response. No graceful degradation is permitted.

## Consequences
* **Positive:** Guaranteed fiscal integrity; no unauthorized token burn during infrastructure distress.
* **Negative:** Potential for localized service denial during transient infrastructure blips (availability tradeoff).
