# ADR 031: Deprecating Redlock for Linearizable Fencing Tokens

## Status
Accepted (Supersedes ADR 011)

## Context
An adversarial Red Team audit identified a critical distributed systems vulnerability in our ADR 011 (Global Fencing for Active-Passive Failover). The architecture relied on a Redis Redlock lease to prevent multi-cloud split-brain double-spending. However, Redlock is vulnerable to clock drift and GC pauses. In a failover scenario, two SAGC regions could temporarily believe they hold the primary lock, leading to unauthorized fiscal spend.

## Decision
We deprecate the Redis Redlock architecture for global fencing.
1. We will transition our global budget state and failover locking to a strictly linearizable database (e.g., Google Cloud Spanner).
2. We will implement **Fencing Tokens**. When a SAGC region acquires the primary lock, it receives a monotonically increasing token (e.g., Token #45). 
3. Every budget deduction write to Spanner must include this token.
4. If a split-brain occurs, and the stale primary attempts to write using Token #45 *after* the new primary has acquired Token #46, the database will mathematically reject the stale write.

## Consequences
* **Positive:** Mathematical guarantee against budget double-spending during catastrophic regional failovers.
* **Negative:** Cloud Spanner introduces significantly higher infrastructure costs and slightly higher latency compared to an in-memory Redis cache.
