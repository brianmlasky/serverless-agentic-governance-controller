# Serverless Agentic Governance Controller

**Real-time cost guardrails for AI workloads on GKE**

An event-driven controller that prevents "token runaway" in LLM applications by enforcing budget policies and autonomously terminating expensive pods. Built with Python AsyncIO, Kyverno admission control, and Kubernetes RBAC.

---

## 🎯 Problem
When you deploy LLM agents on Kubernetes:
- A single misconfigured prompt loop can cost $10k+ in minutes.
- By the time you see the bill, the damage is done.
- You lack real-time infrastructure controls to halt runaway AI processes.

## ✅ Solution
This controller acts as an automated "Fiscal SecOps" layer:
1. **Detects:** Monitors token/cost telemetry in real-time.
2. **Evaluates:** Compares usage against configurable budget policies.
3. **Enforces:** Integrates Kyverno admission control to gate new deployments.
4. **Remediates:** Autonomously executes "kill-switch" pod deletions for violators.
5. **Audits:** Generates a compliance trail for every fiscal decision.

---

## 🏗️ Architecture

graph LR
    User[AI Agent/User] --> Proxy[Governance Controller]
    subgraph "Control Plane"
        Proxy --> Budget{Policy Check}
        Budget -->|Authorized| Upstream[Inference API]
        Budget -->|Denied| Error[403 Forbidden]
    end
    Proxy --> Metrics[Prometheus Metrics]
    Budget -.-> Store[budget.json]

## 📦 Key Components

| Component | Purpose | Tech |
| :--- | :--- | :--- |
| **Event Ingestion** | Receive token/cost signals | Python httpx, event queue |
| **Policy Engine** | Check budget & quotas | Custom Evaluator Logic |
| **Admission Control** | Pre-execution security gates | Kyverno ClusterPolicy |
| **Remediation** | Terminate expensive pods | Kubernetes API |
| **State Persistence** | Restart-safe decisions | ConfigMap Snapshots |
| **Observability** | Structured logging & auditing | JSON logs, Prometheus |

---

## 🚀 Getting Started

### Prerequisites
- GKE 1.27+ with Workload Identity enabled.
- `kubectl`, `gcloud`, and `helm` CLI tools.

### Deployment (Quick Start)
```bash
# 1. Clone & navigate
git clone [https://github.com/brianmlasky/serverless-agentic-platform.git](https://github.com/brianmlasky/serverless-agentic-platform.git)
cd serverless-agentic-platform

# 2. Deploy infrastructure & controller
bash scripts/install.sh

🔐 Security & RBAC
Built on the principle of Least Privilege:

Controller Permissions: Limited to reading/deleting pods in governed=true namespaces.

Workload Identity: No long-lived GCP service account keys; utilizes ephemeral GKE KSA-GSA binding.

Vulnerability Scanning: CI/CD pipeline integrated with Trivy and Bandit to ensure secure supply chain.

🧪 Testing & Validation
The project includes a comprehensive test suite to ensure platform reliability:

Unit Tests: pytest with >80% coverage on evaluation logic.

Integration Tests: Validates pod lifecycle management and ConfigMap state.

Load Tests: Validates event processing latency and throughput under high QPS.

Bash
# Run full suite
pytest src/tests/ -v --cov=src
🗺️ Roadmap
[ ] Multi-cloud support (AWS EKS, Azure AKS)

[ ] ML-driven anomaly detection

[ ] Automated Grafana dashboard generation

[ ] Cost forecasting integration

👨‍💼 Author
Brian Lasky | Cloud Architect & SRE
Specializing in Agentic Infrastructure, Fiscal Governance, and Scalable Cloud Systems.

Website

LinkedIn

GitHub

Status: Production Ready | Last Updated: May 2026
# 3. Verify deployment
kubectl get pods -n governance-system
