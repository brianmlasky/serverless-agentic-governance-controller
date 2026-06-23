# ADR-043: Memorystore Redis Validation for Real-Time Identity Tracking

## Status
Accepted

## Context
While ADR-031 establishes Google Cloud Spanner as the ultimate consistency anchor for linearizable fencing tokens during regional failover, the system requires a sub-millisecond, low-latency cache for localized, real-time transaction tracking (TPM/RPM limits and semantic caching). 

## Decision
We utilize a dedicated Google Cloud Memorystore (Redis) instance running in the `agentic` namespace (`10.252.189.75`). This instance tracks real-time model usage metrics and enforces sub-millisecond rate-limiting gates before egress traffic hits the internet.

## Verification & Key Ledger Structure
Successful integration testing validated that the out-of-process Envoy/LiteLLM pipeline populates the following atomic keys upon intercepting an agent request:
1. `{end_user:sagc-agent-01}:tokens` - Granular, identity-bound consumption ledger.
2. `global_router:...:tpm:<minute>` - Real-time tokens-per-minute circuit breaker tracking.
3. `<sha256_payload_hash>` - Semantic caching layer to prevent duplicate outbound OpEx spend.

## Consequences
- **Positive:** Sub-millisecond latency for real-time traffic interception and rate-limiting enforcement.
- **Positive:** Clean decoupling of localized high-throughput tracking (Redis) from long-term consistent auditing (Spanner).
- **Negative:** Requires strict VPC peering configuration to prevent network isolation between the GKE Autopilot clusters and the Memorystore network plane.