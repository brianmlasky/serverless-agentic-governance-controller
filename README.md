# Serverless Agentic Governance Controller

[![CI/Lint/Test](https://github.com/brianmlasky/serverless-agentic-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/brianmlasky/serverless-agentic-platform/actions/workflows/ci.yml)
[![Security Scan](https://github.com/brianmlasky/serverless-agentic-platform/actions/workflows/security.yml/badge.svg)](https://github.com/brianmlasky/serverless-agentic-platform/actions/workflows/security.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/brianmlasky/serverless-agentic-platform/commits/main)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-January%202025-brightgreen)](https://github.com/brianmlasky/serverless-agentic-platform)

**Autonomous fiscal guardrails for AI workloads on GKE (1.27+)**

An event-driven SRE platform that mitigates "token runaway risk" in LLM applications through closed-loop governance, real-time policy enforcement, and autonomous remediation. Designed for teams deploying GenAI agents on Kubernetes with budget constraints and compliance requirements (SOC2, ISO27001).

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Testing](#-testing)
- [Security](#-security)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Author](#-author)

---

## 🎯 Overview

### Problem Statement

Modern LLM-powered applications deployed on Kubernetes face unpredictable token usage and cost escalation:

- **Token Runaway**: A single misconfigured agent or prompt loop can consume $100k+ in API credits in minutes
- **No Real-Time Controls**: Traditional budget monitoring is reactive; by the time you see the overage, damage is done
- **Compliance Blind Spots**: Auditors need proof of who triggered what workload and what guardrails were applied
- **Multi-Team Friction**: Different teams have different budget allowances and risk profiles; enforcing policy at cluster level is blunt

### Solution

**Serverless Agentic Governance Controller** is a **closed-loop governance system** that:

✅ **Detects** token usage in real-time  
✅ **Evaluates** against policy (budget, quota, risk scores)  
✅ **Enforces** via Kubernetes admission control (Kyverno) + RBAC  
✅ **Remediates** autonomously (kill-switch, pod eviction, quarantine)  
✅ **Audits** every decision for compliance & cost attribution  

### Key Features

| Feature | Benefit |
|---------|---------|
| **Event-Driven Architecture** | Sub-100ms response to cost anomalies; no polling overhead |
| **Closed-Loop Governance** | Policy → Evaluation → Enforcement → Observability → Feedback |
| **Kyverno-Powered Admission Control** | Pre-execution compliance gates; no runtimes slips |
| **Workload Identity** | Least-privilege GCP integration; no service account keys |
| **ConfigMap State Persistence** | Controller restarts don't lose governance decisions |
| **Autonomous Remediation** | Kill-switch and quarantine without human intervention |
| **Multi-Tenant Ready** | Namespace-scoped policies; budget isolation per team |
| **Audit Trail** | Immutable log of all governance actions for SOC2/ISO27001 |
| **Cost Attribution** | Tag every pod action to team, project, and cost center |

---

## 🏗️ Architecture

![Serverless Agentic Governance Controller Architecture](assets/architecture-diagram.png)

*Closed-loop fiscal guardrails for AI workloads on GKE*

### Control Flow

[AI Workloads] ↓ telemetry (tokens, latency, cost) [Governance Controller] (Python AsyncIO event loop) ↓ evaluate (policy, budget, quota, risk assessment) [Policy Engine] (Kyverno + RBAC) ↓ enforce (admission control, authorization) [Autonomous Remediation] (kill-switch, rollback, quarantine) ↓ [Observability + Audit] (logs, metrics, alerts, compliance trail)


### Primary Control Loop

| Component | Function | Technology |
|-----------|----------|-----------|
| **AI Workloads** | Models, prompts, agents emitting telemetry | Any LLM framework (LiteLLM, LangChain, etc.) |
| **Telemetry + Usage Events** | Token count, execution latency, cost signals | Structured JSON events to event bus |
| **Governance Controller** | Event ingestion, state management, policy orchestration | Python 3.10+ with AsyncIO, httpx, kubernetes-client |
| **Policy Evaluation** | Budget thresholds, quota limits, risk scoring | Custom evaluator + Kyverno policy engine |
| **Kyverno + RBAC** | Admission control at cluster boundary, authorization scopes | Kyverno 1.10+, Kubernetes RBAC |

### Supporting Controls

| Layer | Purpose | Mechanisms |
|-------|---------|-----------|
| **State Persistence** | Restart-safe governance decisions | ConfigMaps, labeled snapshots |
| **Budget Guardrails** | Cost enforcement | Threshold triggers, quota enforcement |
| **Admission Control** | Pre-execution compliance gates | Kyverno ClusterPolicy, namespace labels |
| **Workload Identity** | Least-privilege service authentication | GKE Workload Identity binding |
| **Autonomous Remediation** | Automatic breach response | Kill-switch (pod deletion), quarantine (label isolation) |

### Observability + Audit

Every decision is observable and auditable:

| Signal | Purpose | Destination |
|--------|---------|-------------|
| **Logs** | Decision traces, remediation history | Cloud Logging (structured JSON) |
| **Metrics** | Token usage, cost delta, violation count, latency | Cloud Monitoring / Prometheus |
| **Alerts** | Threshold breaches, kill-switch triggers, RBAC denials | Cloud Alerting, Slack, PagerDuty |
| **Audit Trail** | Immutable record of all governance actions | Cloud Audit Logs |
| **Executive Visibility** | Compliance reporting, cost trends | Grafana dashboards, monthly reviews |

### Key Design Principles

✅ **Event-Driven**: Reacts to telemetry in <100ms  
✅ **Idempotent**: Safe to replay without duplicate enforcement  
✅ **Policy-as-Code**: Governance defined in Kubernetes YAML  
✅ **Least Privilege**: Scoped identity, minimal RBAC blast radius  
✅ **Resilient**: State persisted; survives controller restarts  
✅ **Auditable**: Full decision trail for compliance review  

---

## 🚀 Quick Start

### Prerequisites

- **GKE Cluster**: 1.27+ with Workload Identity enabled
- **Local Tools**: `kubectl` (1.27+), `gcloud` CLI, `git`, `python3.10+`
- **Permissions**: Cluster admin for initial setup

### 60-Second Deployment

```bash
# 1. Clone the repository
git clone https://github.com/brianmlasky/serverless-agentic-platform.git
cd serverless-agentic-platform

# 2. Set environment variables
export PROJECT_ID=$(gcloud config get-value project)
export CLUSTER_NAME="your-gke-cluster"
export REGION="us-central1"

# 3. Get cluster credentials
gcloud container clusters get-credentials $CLUSTER_NAME --region=$REGION

# 4. Run installation script (installs Kyverno + controller)
bash ./scripts/install.sh

# 5. Verify deployment
kubectl get pods -n governance-system
kubectl logs -n governance-system -l app=governance-controller --tail=10

# ✅ Done! Your cluster is now governed.
