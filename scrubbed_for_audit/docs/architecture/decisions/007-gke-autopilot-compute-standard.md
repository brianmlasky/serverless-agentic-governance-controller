# ADR 007: GKE Autopilot Selection for Fiscal Agentic Compute

## Status
Accepted

## Context
The platform requires a highly elastic container orchestration layer capable of running long-lived multi-agent frameworks, sidecar proxies (LiteLLM), and real-time governance controllers. We evaluated three compute paradigms:
1. **Cloud Run (Serverless Container):** Excellent for HTTP microservices, but restricted by hard timeout boundaries, lack of native service mesh orchestration capabilities, and costly execution over extended agent runtimes.
2. **GKE Standard (Managed Kubernetes):** Full control over node architectures, but introduces significant management overhead and "idle capacity tax" where the organization pays for unutilized virtual machines during periods of agent dormancy.
3. **GKE Autopilot (Fully Managed Kubernetes):** Abstracts node provisioning while keeping the native Kubernetes API intact. Charges are applied strictly per-pod based on provisioned vCPU, memory, and storage resource requests.

## Decision
We select GKE Autopilot as the foundational compute engine for the Serverless Agentic Governance Controller platform. 
* **Fiscal SecOps Alignment:** Eliminates operational expenditure on idle compute pools, ensuring our cost curve maps linearly to actual agent runtime execution.
* **Reduced Management Overhead:** Day-2 operations (node upgrading, patching, OS hardening) are fully offloaded to Google, freeing internal engineering resources to focus entirely on agent governance logic.

## Consequences
* **Positive:** Zero cost overhead for idle infrastructure capacity.
* **Positive:** Automatic adherence to Google Cloud secure node baseline configurations.
* **Negative:** Restricts the use of low-level cluster mutations (e.g., custom node taints or privileged daemonsets), requiring all governance controls to be executed purely via application-layer controllers and admission webhooks.