# Architecture: Serverless Agentic Governance Controller (SAGC)

## 📖 Overview
The SAGC is an infrastructure-level admission controller designed for autonomous AI workloads running on Serverless Kubernetes (GKE Autopilot). It intercepts outbound LLM inference requests at the network layer, executing mathematical fiscal governance via Open Policy Agent (OPA) to prevent infinite-loop token burn.

## 🏗️ System Components

1. **The Workload:** AI agents containerized and running within Kubernetes pods.
2. **The Interceptor (Envoy/Sidecar):** A network proxy injected into the agent pod that intercepts all egress HTTP traffic destined for LLM providers (e.g., OpenAI, Vertex AI).
3. **The Policy Engine (Open Policy Agent):** An OPA container running alongside the proxy. It evaluates the outbound request against locally cached budget policies.
4. **The Telemetry Stack (Prometheus):** Scrapes the sidecars for `x-sagc-tokens-consumed` and `budget_exhaustion_events` to provide real-time dashboarding.
5. **Infrastructure as Code (Terraform):** The entire stack, including Workload Identity Federation (WIF) and GKE Autopilot clusters, is provisioned via idempotent Terraform modules.

## 🚦 The Control Flow

1. **The Request:** An AI agent attempts to send a prompt to the OpenAI API.
2. **The Interception:** The sidecar proxy traps the outbound request before it leaves the pod network.
3. **Policy Evaluation (Rego):** The proxy asks OPA, "Does this workload have sufficient budget to execute?" OPA evaluates its Rego policies and the current atomic budget state.
4. **Fail-Closed Enforcement:** * *Authorized:* The proxy forwards the request to the LLM.
   * *Denied:* The proxy drops the packet, returning a `402 Payment Required` to the agent.
5. **Settlement & Observability:** Post-execution, the exact token usage is parsed from the LLM response headers, the budget state is decremented, and Prometheus scrapes the updated metrics.

## 🛡️ Key Architectural Decisions (ADRs)

* **Network-Level Enforcement over Application Logic:** Elected to use a sidecar proxy rather than requiring developers to import a specific SDK. This ensures governance is mathematically enforced regardless of what language (Python, Node, Go) the agent is written in.
* **Open Policy Agent (OPA):** Chose OPA for Policy-as-Code to decouple business governance rules from the proxy routing logic, allowing security teams to audit Rego files via GitOps.
* **GKE Autopilot (Serverless K8s):** Deployed on GKE Autopilot to abstract node management and auto-scaling, maintaining a serverless operational footprint while leveraging standard Kubernetes admission controllers.