# Serverless Agentic Governance Controller (SAGC)

**Active governance and fiscal oversight for autonomous AI workloads.**

---

## Architecture Overview

The SAGC functions as an **Admission Control Middleware**, intercepting inference requests to validate fiscal authorization in real-time.

![SAGC Architecture Diagram](./assets/sagc-architecture.jpg)

## Core Capabilities

* **Fail-Closed Security:** Defaults to blocking traffic if policy validation fails or the budget store is inaccessible.
* **Fiscal Observability:** Built-in Prometheus instrumentation provides real-time "Token Burn Rate" telemetry.
* **Atomic State Consistency:** Thread-safe, atomic I/O operations ensure budget integrity.
* **Policy-as-Code:** Governance logic is decoupled from business logic, allowing for Git-based auditing.

## Quick Start

```bash
# Install dependencies
make install

# Start the governance controller
make run

Resilience & Operational Readiness
This controller is designed for high-availability, cloud-native environments.

Auditability: Budget states are persisted as version-controlled artifacts.

Scalability: Designed for sidecar container deployment within Kubernetes clusters.

Repository Organization Standard
To ensure rapid response during an incident (e.g., a developer looking for answers at 3 AM), this repository is strictly organized into the following knowledge domains:

Incident Response: /docs/playbooks/ (e.g., failure-scenarios.md). Contains actionable, step-by-step recovery procedures.

Engineering Rules: /docs/architecture/ (e.g., standards.md). Contains structural standards, patterns, and framework evaluation criteria.

Decision Frameworks: /docs/adr/ (e.g., README.md). Contains Architecture Decision Records detailing the business and technical rationale behind major platform shifts.

Maintained by Brian Lasky | Senior SRE
