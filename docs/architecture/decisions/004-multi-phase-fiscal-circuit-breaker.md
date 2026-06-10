# ADR 004: Multi-Phase Fiscal Circuit Breaker (The Brownout Strategy)

## Status
Accepted - Phase 3 (Hard Kill) Implemented. Phases 1 & 2 Planned.

## Context
Autonomous LLM agents present a unique financial vulnerability: "token runaway." If an agent enters an infinite loop or encounters a malformed prompt array, it can exhaust enterprise API budgets within minutes. 

While a strict `sys.exit(1)` kill-switch mathematically guarantees budget containment (Fail-Closed), executing a hard termination without warning introduces severe operational friction. Application teams lose critical telemetry and often misdiagnose infrastructure-enforced terminations as memory leaks or application crashes.

## Decision
We will implement a 3-Phase "Brownout Strategy" for the Serverless Agentic Governance Controller to gracefully degrade service before enforcing a hard boundary.

*   **Phase 1: Asynchronous Alerting (80% Threshold)**
    *   **Action:** The controller dispatches an asynchronous webhook to the platform engineering observability stack (Slack/PagerDuty) indicating budget exhaustion is imminent.
    *   **Intent:** Provide human operators a window to intervene, raise the budget, or gracefully cordon the workload.
*   **Phase 2: Inference Throttling (90% Threshold)**
    *   **Action:** The proxy injects artificial latency into outbound LLM API requests using a token-bucket rate-limiting algorithm.
    *   **Intent:** Throttle concurrency to slow the burn rate without severing the compute node, allowing critical, slow-path operations to complete.
*   **Phase 3: Fail-Closed Termination (100% Threshold)**
    *   **Action:** The controller executes a `sys.exit(1)`, severing the container lifecycle.
    *   **Intent:** The absolute, mathematically enforced zero-trust fiscal boundary. Kubernetes will attempt a restart, but admission will fail if the budget is not cleared.

## Consequences
*   **Positive:** We guarantee a $0.00 footprint baseline during runaway events. We preserve developer experience by providing telemetry before termination.
*   **Negative:** Throttling (Phase 2) introduces complexity into the proxy layer and requires stateful tracking of token consumption across clustered pods.