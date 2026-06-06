# SRE Spec 001: Core SLA / SLO / SLI Definitions

## 1. LiteLLM Proxy Gateway Metrics
* **Service Level Indicator (SLI):** HTTP 5xx error rate and P95 latency for token generation requests passing through the proxy.
* **Service Level Objective (SLO):** * Error Rate: < 0.5% over a rolling 7-day window.
  * Latency: P95 < 250ms overhead added to the base LLM API response time.
* **Error Budget:** 21 minutes of allowable degradation per 30-day window. If depleted, feature deployments freeze.

## 2. Infrastructure Metrics
* **SLI:** GKE Autopilot Pod scheduling and startup latency.
* **SLO:** 99% of new agentic pods must transition from `Pending` to `Running` within 45 seconds to ensure real-time governance responsiveness.