# ADR 033: Transitioning to Linearizable Atomic Deductions

## Status
Proposed

## Context
While ADR 031 identified Spanner as the target for global fencing, budget constraints necessitate a $0.00 infrastructure spend. Our current local budget deduction logic relies on an optimistic update pattern, creating a window for "fiscal slippage" during high-velocity agentic bursts.

## Decision
To ensure end-to-end fiscal integrity without incurring cloud database costs: 
1. We will implement application-level atomic Read-Modify-Write (RMW) transactions using Redis `EVAL` (Lua scripting).
2. All budget decrements will be processed as atomic Lua scripts to guarantee serializability within the existing Redis infrastructure.
3. We will enforce "Fencing Tokens" within the Lua script to reject stale writes, effectively replicating the linearizable guarantee of ADR 031 at the application layer.
4. We will deprecate local, loosely consistent caching in favor of direct interaction with the Redis atomic state.

## Technical Debt
* **Spanner Dependency:** This ADR intentionally deviates from the Spanner requirement in ADR 031 to maintain a $0.00 cost profile.
* **Risk:** Unlike Spanner's native ACID guarantees, this approach relies on the reliability of the Redis deployment. Regional failovers may require manual state reconciliation if Redis replication lag occurs.

## Consequences
* **Positive:** Achieves linearizable fiscal integrity at $0.00 additional cost; eliminates fiscal slippage via Lua atomicity.
* **Negative:** Moves the burden of consistency from the database layer to the application layer; requires rigorous testing of Lua scripts.

## Update (2026-06-22): Cryptographic Fencing
To mitigate replay attacks identified in the 2026-06-22 Adversarial Audit, we are deprecating simple monotonic tokens. All fencing tokens must now be HMAC-SHA256 signatures derived from a server-side secret, bound to an `agent_id` and a 5-minute expiry window.
