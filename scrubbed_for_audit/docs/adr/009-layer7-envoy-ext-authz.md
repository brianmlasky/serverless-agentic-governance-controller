# ADR 009: Layer 7 Interception via Envoy Ext_Authz

## Status
Accepted

## Context & Problem
We possess OPA Rego policies (ADR 007) capable of enforcing fiscal budgets. However, AI agents written in different languages (Python, Node, Go) construct outbound HTTP calls differently. Relying on application-level routing to reach OPA introduces bypass risks.

## Decision
We will manipulate the data plane directly using an **EnvoyFilter**. 
We inject the `envoy.filters.http.ext_authz` filter into the `SIDECAR_OUTBOUND` context. Every outbound L7 request is paused and evaluated against the local OPA sidecar (`localhost:9191`) via a gRPC handshake before routing to the internet.

## Consequences
* **Positive:** Complete language agnosticism. Developers cannot bypass the proxy.
* **Positive (Fail-Closed):** Configured `failure_mode_allow: false`. If the OPA sidecar crashes or the 250ms timeout is breached, Envoy drops the traffic. The business is protected from infrastructure faults.
* **Negative:** Adds up to 250ms of maximum latency to outbound LLM requests (acceptable tradeoff for asynchronous AI workloads).
