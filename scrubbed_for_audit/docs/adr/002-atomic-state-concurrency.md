# ADR 002: Atomic State Management for Budget Concurrency

**Date:** 2026-06-05
**Status:** Accepted
**Primary Business Driver:** Prevent fiscal overspend (Race Conditions) during high-concurrency AI inference spikes.

## Context
The Serverless Agentic Governance Controller (SAGC) acts as the fiscal circuit breaker for autonomous AI agents. In a production environment, an agentic workload may horizontally scale to dozens of concurrent pods. 

If multiple pods attempt to deduct tokens from the same `Workload Identity` budget simultaneously, a standard "Read-Modify-Write" pattern will result in a Race Condition. Multiple requests will read the same remaining balance before the database is updated, causing the system to authorize requests that collectively exceed the hard budget cap.

## Decision
We will reject standard relational database updates (e.g., SQL `UPDATE` with row locks) and in-memory state tracking. Instead, the SAGC will rely exclusively on a centralized, highly-available key-value store (e.g., Redis) utilizing **Atomic Decrement Operations** (e.g., `DECRBY`) or a NoSQL datastore (e.g., DynamoDB/Firestore) utilizing **Optimistic Concurrency Control (OCC)**.

## Considered Alternatives
1.  **In-Memory State (Rejected):** Tracking the budget in the RAM of the SAGC sidecar. *Why rejected:* State is lost if the pod restarts. More importantly, budget state cannot be shared across multiple horizontal replicas of the agent, rendering global budget caps impossible.
2.  **Relational SQL DB with Pessimistic Locking (Rejected):** Using `SELECT ... FOR UPDATE` to lock the budget row until the transaction completes. *Why rejected:* Pessimistic locking introduces unacceptable latency. If 50 agents hit the database, 49 must wait in a queue, causing cascading timeouts in the inference pipeline.

## Rationale
* **Atomic Precision:** An atomic operation (like Redis `DECRBY`) ensures that reading the current budget and deducting the new token count happens as a single, indivisible computational step. It is mathematically impossible for two concurrent network requests to read the same stale state.
* **Low Latency:** Distributed key-value stores optimized for atomic operations provide sub-millisecond response times, ensuring the fiscal check does not degrade the application's overall performance SLA.

## Consequences (Trade-offs)
* **Positive:** Complete elimination of race-condition-induced overspending. The fiscal boundary is mathematically guaranteed regardless of cluster scale.
* **Negative:** Introduces a strict infrastructure dependency on a highly-available centralized cache/state-store. If the centralized state store experiences an outage, the SAGC defaults to `Fail-Closed`, potentially causing a system-wide denial of service for outbound AI requests.

## Future Considerations (Deferred Decisions)
* To mitigate the risk of the centralized state store becoming a single point of failure (SPOF), future iterations may implement a "Local Token Bucket" architecture. In this model, the centralized store allocates "chunks" of the budget (e.g., $5.00 blocks) to the local SAGC sidecars periodically, allowing them to perform local atomic deductions and survive temporary network partitions from the main database.
