# ADR 034: Budget State Reconstruction from Immutable Audit Logs

## Status
Proposed

## Context
ADR 033 moved our atomic fiscal state to an application-level Redis/Upstash implementation. Because this lacks the native durability/linearizability of Spanner, a total cache loss event (e.g., Redis cluster flush) would result in a "fiscal blackout" where current agent token balances are lost, preventing safe system resumption.

## Decision
We will treat our immutable audit log bucket (ADR 014) as the authoritative "long-term ledger" for the SAGC budget state.
1. In the event of a cache loss, the system will trigger a "State Recovery" routine.
2. The recovery routine will stream the last N events from the `sagc-audit-logs-immutable` bucket.
3. The system will replay the fiscal events (deductions and top-ups) to reconstruct the `remaining_tokens` balance for all active agents.
4. The Redis state will be repopulated only after the replay completes, ensuring the system resumes from a mathematically verified balance.

## Consequences
* **Positive:** Provides a zero-cost disaster recovery mechanism that leverages existing storage; eliminates the need for expensive cross-region Redis replication.
* **Negative:** Recovery time (RTO) increases as the number of agents and transaction volume grows; requires a specialized replay script to be maintained.