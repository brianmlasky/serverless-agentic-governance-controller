# ADR-006: Observability-as-Code and Telemetry Standard

## Status
Accepted

## Context
The Serverless Agentic Governance Controller (SAGC) enforces critical fiscal boundaries. Operational transparency into its decision-making (e.g., token burn rates, OPA evaluation latency, circuit breaker trips) is required for FinOps and SRE teams. Manually configuring dashboards creates operational toil and configuration drift across environments.

## Decision
We will implement an "Observability-as-Code" standard using the Prometheus/Grafana stack:
1. **Prometheus ServiceMonitor:** A declarative Kubernetes custom resource will automatically discover and scrape the SAGC `/metrics` endpoint.
2. **Grafana Dashboards:** Visualizations will be stored as JSON artifacts in the repository and provisioned dynamically via Grafana provisioning sidecars or GitOps (ArgoCD).

## Consequences
* **Positive:** Instant operational visibility upon deployment. Dashboards are version-controlled and undergo the same PR review process as application code.
* **Negative:** Introduces a dependency on the Prometheus Operator being present in the target Kubernetes cluster for the `ServiceMonitor` to function.

## FinOps Telemetry Philosophy (Amendment to ADR 006)
To prevent alert fatigue and ensure systemic understanding, we adopt a "Dollar-Aware Observability" posture:
* **Metric-First:** We avoid high-cardinality log-streaming for routine blocks. We aggregate at the Envoy edge via Prometheus counters.
* **Causal Linking:** All alerts must point to the specific business value being protected (e.g., "Budget Guardrail Tripped = $X saved from potential runaway loop").
* **Cognitive Load:** Dashboards must include "Runbook Context" fields. Any engineer on-call should be able to look at a Grafana panel and see the exact ADR and policy logic that generated that metric.