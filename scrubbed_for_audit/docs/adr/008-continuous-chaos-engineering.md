# ADR 008: Continuous Chaos Engineering for Fiscal Guardrails

## Status
Accepted

## Context & Problem
Traditional unit tests mock external dependencies, ensuring code logic is correct but ignoring systemic network behavior. In an active-passive multi-cloud environment, a race condition in the OPA sidecar or database layer could allow an agent to bypass the budget limit if 50 concurrent threads request execution simultaneously.

## Decision
We will mandate **Continuous Chaos Engineering** as an absolute deployment gate. The `make test-chaos` suite utilizes highly concurrent thread pools (`concurrent.futures`) to aggressively bombard the Envoy egress proxy.

* **Assertion:** The pipeline is only marked 'Green' if the proxy successfully intercepts the traffic and returns an `HTTP 429` under load.
* **Execution:** This test runs against ephemerally provisioned infrastructure mimicking the production GKE Autopilot environment.

## Consequences
* **Positive:** Mathematically proves our atomic state concurrency (ADR 002) holds up under live network saturation.
* **Positive:** Prevents regressions where a misconfigured Envoy filter accidentally allows traffic to bypass OPA.
* **Negative:** CI/CD pipeline execution time increases slightly due to deliberate network stress testing.
