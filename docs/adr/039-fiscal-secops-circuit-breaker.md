# ADR 039: Fiscal SecOps Circuit Breaker & Workload Termination

## Status
Accepted

## Context
Autonomous agentic workloads inherently possess the risk of entering unbounded recursive loops (e.g., hallucination cycles or rapid API retry storms). Traditional API rate limiting (HTTP 429) is insufficient for Fiscal SecOps, as a runaway agent may continuously retry, burning through available compute and network resources even if external LLM provider calls are blocked. We require a deterministic, fail-closed mechanism to physically halt the offending workload and protect the organizational cloud budget.

## Decision
We are implementing a hard circuit breaker pattern utilizing the HA-Memorystore backend to track real-time token burn and enforce atomic budget states:

1.  **High-Frequency Telemetry:** The SAGC sidecar intercepts all egress traffic to LLM providers, calculating the `token_burn_rate` via asynchronous Redis counters (ZSETs) evaluated over a sliding window.
2.  **Deterministic Pod Termination (SIGTERM):** If an agent's burn rate exceeds the predefined fiscal threshold (e.g., >1,000 tokens/sec) or exhausts its atomic budget, the controller issues an immediate HTTP 403 (Fail-Closed) to the current request.
3.  **Workload Eviction:** Simultaneously, the SAGC triggers a Kubernetes API call to issue a `SIGTERM` directly to the offending agent pod, physically killing the runaway process and forcing a clean restart state.
4.  **State Persistence:** The budget exhaustion state is locked in Redis. Restarted pods will immediately encounter a "Budget Exhausted" denial until the fiscal policy is manually reset or time-decayed.

## Consequences
* **Positive:** Provides absolute fiscal certainty. Runaway AI token spend is mechanically impossible due to the hard termination of the compute environment.
* **Positive:** Satisfies the strict "Fail-Closed Posture" established in ADR 036.
* **Negative:** Legitimate agent workloads experiencing sudden, valid spikes in complexity may be ruthlessly terminated (killed mid-thought), requiring robust application-level retry-and-resume logic upon pod restart.