# ADR 036: Fail-Closed Posture and Volumetric Degradation

**Status:** Accepted
**Date:** 2026-06-23

## Context and Problem Statement
When orchestrating autonomous AI agents, a runaway recursive loop or a volumetric traffic spike can rapidly consume cloud compute and LLM token budgets. If the governance gateway (LiteLLM) fails to process state or loses connection to its backend, the system must definitively prioritize budget preservation over uptime. How do we ensure the gateway degrades securely under extreme load without leaking tokens or passing unauthenticated traffic?

## Decision
We will enforce a strict Fail-Closed posture across all layers of the Serverless Agentic Governance Controller:

1. **Application-Layer Circuit Breaking (HTTP 429):** Sequential, high-velocity anomalous requests that breach the atomic budget state will be intercepted by the middleware, returning `HTTP 429 Too Many Requests` to the autonomous agent rather than forwarding the payload to upstream providers (e.g., AWS Bedrock).
2. **Volumetric Connection Dropping (TCP Reset):** Under extreme concurrent flooding (e.g., 50+ simultaneous unauthorized worker spawns), the Uvicorn ASGI server is intentionally constrained by memory limits (`1Gi`) and worker pool limits. It will aggressively sever TCP connections (`Connection reset by peer`) rather than buffer requests. 

## Consequences
* **Positive:** Complete elimination of runaway token spend during catastrophic agentic loops. Secure degradation is achieved without crashing the container or requiring control-plane intervention.
* **Negative:** Legitimate traffic spikes that exceed the Uvicorn connection pool will be dropped rather than queued. This requires upstream clients to implement exponential backoff and retry logic.