# ADR 041: Redis-Backed Atomic Budget State

**Status:** Accepted
**Date:** 2026-06-23

## Context and Problem Statement
To enforce the "Fail-Closed Posture" defined in ADR 036 and the "Circuit Breaker" mechanism in ADR 039, we require a persistent, cluster-wide source of truth for token consumption. Our previous stateless implementation in LiteLLM is insufficient for distributed workloads across multiple GKE pods. How do we ensure that token budget limits are respected globally, even when agentic tasks are distributed across a dynamic compute fleet?

## Decision
We are adopting a centralized, high-availability Redis Memorystore instance to act as the atomic state store for the Serverless Agentic Governance Controller (SAGC).

1. **Atomic State Mapping:** Every agentic request is tagged with a `project_id` and `agent_identity`. Token usage is tracked via Redis `INCRBY` operations, ensuring atomicity across concurrent requests.
2. **Persistence Strategy:** Budget states are persisted with a TTL (Time-To-Live) aligned with the organizational financial cycle (e.g., 24-hour windows).
3. **Connectivity:** The LiteLLM gateway sidecar establishes a secure connection to the Memorystore endpoint using VPC-SC (Service Controls) to ensure data-in-transit security.

## Consequences
* **Positive:** Real-time visibility into token burn across the entire fleet; provides a robust foundation for automated "Fiscal SecOps" policy enforcement.
* **Positive:** Decouples budget state from the compute lifecycle, allowing for seamless pod scaling without risking budget overruns.
* **Negative:** Introduces a dependency on Redis availability. We must implement circuit breaking within the gateway to "Fail-Closed" if the state-store becomes unreachable to prevent uncontrolled AI inference.