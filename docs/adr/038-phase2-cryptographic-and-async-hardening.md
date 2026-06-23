# ADR 038: Phase 2 Cryptographic, Asynchronous, and Identity Hardening

## Status
**Accepted** (Implemented via Phase 2 Remediation)

## Context
A Phase 2 Adversarial Security Audit identified four critical vulnerabilities in the Serverless Agentic Governance Controller (SAGC) that could lead to cascading infrastructure failure or fiscal compromise under heavy production load:
1.  **F1 (Token Recomputation Race):** Predictable token generation allowed for offline chosen-plaintext attacks.
2.  **F2 (Worker Pool Starvation):** Synchronous Redis I/O within the FastAPI event loop caused worker thread exhaustion during network brownouts.
3.  **F3 (ZSET Memory Leak):** Pipelined Redis commands without atomic execution guarantees led to orphaned keys and unbounded memory growth.
4.  **F4 (NetworkPolicy Label Spoofing):** Reliance on mutable Kubernetes pod labels for network isolation allowed for privilege escalation via pod restart races.

## Decision
To ensure production-grade fault tolerance and Zero-Trust security, we implemented the following architectural mandates:

1.  **Cryptographic Nonce Commitments (F1):** Fencing tokens must now incorporate a 128-bit server-side nonce (CSPRNG). The nonce is stored in Redis with a 5-minute TTL and is atomically consumed upon validation to mathematically prevent replay and precomputation attacks.
2.  **Strict Asynchronous I/O & Circuit Breaking (F2):** The governance sidecar must use `redis.asyncio` exclusively. All external state calls are wrapped in a Circuit Breaker pattern with a strict 3.0-second timeout to fast-fail and protect the ASGI worker pool.
3.  **Atomic Lua State Mutations (F3):** All multi-step Redis operations (rate limiting, budget deductions, and TTL expirations) are executed via pre-compiled, atomic Lua scripts (`evalsha`). This guarantees ACID compliance and prevents memory leaks during network partitions.
4.  **Immutable Identity Network Binding (F4):** Kubernetes `NetworkPolicy` ingress and egress rules are bound strictly to `serviceAccountSelectors` rather than `podSelectors`. Pod label mutation is no longer a viable network bypass vector.

## Consequences
* **Positive:** The SAGC is now mathematically immune to offline HMAC forgery, immune to ASGI worker starvation, and structurally isolated at the CNI layer. 
* **Positive:** Graceful degradation is achieved; Redis outages result in immediate HTTP 403 (Fail-Closed) rather than cascading HTTP 500s.
* **Negative/Constraint:** Infrastructure deployments must rigidly adhere to ServiceAccount provisioning. Local testing requires a running asynchronous Redis instance.
