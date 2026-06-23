# Security Remediation Ledger: Phase 2 (Production Hardening)
**Date:** 2026-06-22  
**System:** Serverless Agentic Governance Controller (SAGC)  
**Focus:** Cryptographic Nonces, Async Worker Starvation, and Memory Leak Prevention  

## 1. Executive Summary
Following the initial adversarial audit (Phase 1), a deeper cryptanalysis and systems-level threat model (Phase 2) revealed critical vulnerabilities in the SAGC's asynchronous handling, cryptographic state machine, and Redis memory management. These "unknown unknowns" presented severe risks of cascading pod failures, OOM crashes, and chosen-plaintext token forgery under heavy load. 

All identified Phase 2 vulnerabilities have been remediated in `main`. The architecture now strictly enforces non-blocking operations, atomic sliding-window rate limits, and server-side cryptographic nonces.

---

## 2. Threat Vectors & Implemented Defenses

### F1: Fencing Token Recomputation Race (Chosen-Plaintext Attack)
* **Vulnerability:** Fencing tokens relied on recomputation of a server-side secret using predictable inputs (previous tokens). This allowed an attacker to conduct an offline dictionary attack to recover the `FENCING_SECRET`, enabling infinite token forgery and boundless budget exhaustion.
* **Remediation:** Migrated from a purely stateless token to a **Cryptographic Nonce Commitment**. The system now generates 128-bit server-side nonces cached in Redis with a 5-minute TTL. The token validation strictly consumes this nonce, rendering replay and offline brute-force attacks mathematically infeasible.

### F2: FastAPI Worker Pool Starvation
* **Vulnerability:** The governance sidecar utilized synchronous Redis calls (`redis.Redis`) inside an asynchronous FastAPI framework. Under simulated Redis brownouts, worker threads blocked indefinitely waiting for socket timeouts. This would cause Kubernetes liveness probes to fail, triggering a catastrophic failover loop across all replica pods.
* **Remediation:** Fully transitioned the pipeline to `redis.asyncio` with explicit connection pooling. Implemented an asynchronous **Circuit Breaker** pattern. If Redis latency spikes or connections drop, the circuit opens, failing-closed immediately to preserve the ASGI worker pool and maintain pod health.

### F3: Redis ZSET Pipeline Partial Failure (Memory Leak)
* **Vulnerability:** The sliding-window rate limiter utilized a standard Redis pipeline for `ZADD`, `ZREMRANGEBYSCORE`, and `EXPIRE`. A network partition mid-pipeline would leave orphaned ZSET keys without a TTL, creating an unmonitored memory leak guaranteed to OOM-kill the Redis instance over a 6-week operational window.
* **Remediation:** Replaced the Python-managed pipeline with a **Pre-compiled Atomic Lua Script**. The rate-limiting logic (`RATE_LIMIT_CHECK_LUA`) is now executed atomically on the Redis server, guaranteeing that TTL expiry commands execute in the same cycle as data ingestion. 

---

## 3. Remediation Impact Matrix

| Finding | Pre-Remediation State | Post-Remediation Architecture | Residual Risk |
| :--- | :--- | :--- | :--- |
| **F1 (Token Forgery)** | 64-bit truncated signature, predictable inputs. | 256-bit HMAC + Server-side consumed Nonce. | None (Requires breaking SHA-256). |
| **F2 (Worker Starvation)** | Synchronous I/O blocks ASGI event loop. | `redis.asyncio` + Circuit Breaker. | Transient request denial during Redis outages (Expected Fail-Closed behavior). |
| **F3 (ZSET Memory Leak)** | Client-side pipeline susceptible to partitions. | Server-side atomic Lua evaluation. | None. |

## 4. Architectural Decisions Enforced
This remediation cycle solidifies the following core tenets of the SAGC infrastructure:
1.  **Strict Fail-Closed:** Network partitions must result in HTTP 503 or 403, never an unmonitored bypass.
2.  **Zero-Trust State:** Client-provided tokens are intrinsically untrusted until cryptographically verified against a server-side commitment.
3.  **Non-Blocking I/O:** Governance middleware must never starve the primary application thread pool.
