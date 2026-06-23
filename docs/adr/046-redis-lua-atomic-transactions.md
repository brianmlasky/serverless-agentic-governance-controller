# ADR-046: Atomic Distributed State via Redis Lua Scripting

## Status
Accepted

## Context
An adversarial architecture audit identified a critical Time-of-Check to Time-of-Use (TOCTOU) race condition between the LiteLLM proxy and the Redis tracking ledger. Under high concurrency, multiple agentic threads could successfully verify an available token budget before the counter increments, resulting in unbounded fiscal overspend (double-spending).

## Decision
All fiscal circuit breaker checks will transition from standard `GET/INCR` operations to single-threaded, atomic **Lua Script execution** within the Memorystore (Redis) engine. 

## Consequences
- **Positive (Security):** The `GET -> COMPARE -> INCR` pipeline executes as a single, indivisible transaction, mathematically preventing budget overruns regardless of concurrent request volume.
- **Positive (Performance):** Executes entirely server-side within the Redis C-engine, eliminating multiple network round-trips from the proxy.
- **Negative (Complexity):** Introduces Lua script management and SHA caching into the proxy codebase.