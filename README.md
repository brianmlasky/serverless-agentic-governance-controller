# Serverless Agentic Governance Controller (SAGC)

**Engineering AI reliability, security, and unit economics at enterprise scale.**

---

## The Problem: The $500K Weekend
Autonomous AI agents are currently being deployed without fiscal circuit breakers. In production operations, I have seen unconstrained agents enter recursive loops, burning hundreds of thousands in cloud spend over a single weekend. 

## The Impact
I architected the SAGC to move governance from "documentation" to "mathematical enforcement."
* **Cost Reduction**: Proven reduction of uncontrolled cloud spend by **60-70%**.
* **Operational Reliability**: Maintained **99.95% uptime** on agentic workloads while enforcing strict budget gating.
* **Audit-Ready**: Moved fiscal governance to the Kubernetes control plane, ensuring every deployment is pre-validated by Policy-as-Code.

---

## Architecture Overview
The SAGC functions as an **Admission Control Middleware**, intercepting inference requests to validate fiscal authorization in real-time. 

## Core Capabilities
* **Fail-Closed Security**: Defaults to blocking traffic if policy validation fails or the budget store is inaccessible.
* **Fiscal Observability**: Built-in Prometheus instrumentation provides real-time "Token Burn Rate" telemetry.
* **Atomic State Consistency**: Thread-safe, atomic I/O operations ensure budget integrity.
* **Policy-as-Code**: Governance logic is decoupled from business logic, allowing for Git-based auditing.

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

🚀 Clean Room Deployment & Verification
This repository is designed for a zero-friction handoff.

Prerequisites
A Google Cloud Project with Workload Identity Federation (WIF) configured.

A Kubernetes cluster (GKE) with the Prometheus Operator installed.

Local dependencies: kubectl, terraform, python3.10+, and make.

Bootstrap Command
To deploy the OPA sidecar, the SAGC controller, and the observability stack:

Bash
kubectl apply -k k8s/
kubectl apply -f monitoring/sagc-service-monitor.yaml
Verification Command
Run the chaos engineering suite to simulate a token runaway event and verify the fail-closed architecture:

Bash
make test-chaos
Expected Result: The script will trigger alerts, inject throttling, and ultimately execute a sys.exit(1) hard kill when the budget hits 100%.

Maintained by Brian Lasky | Senior Site Reliability Engineer & Cloud Architect
## Architectural Defense & Stakeholder Alignment
A production-grade system must be defended against both technical failure and business risk. I have compiled an exhaustive Pre-Mortem and Stakeholder Q&A matrix that addresses the strategic, financial, and operational implications of the Serverless Agentic Governance Controller.

* 📖 **[Read the Full Stakeholder Q&A Matrix](docs/interview/stakeholder-qa.md)**
