# Serverless Agentic Governance Controller (SAGC)

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Passing-brightgreen) ![Architecture](https://img.shields.io/badge/Architecture-Event--Driven-blue) ![Compliance](https://img.shields.io/badge/Compliance-SOC2%20Ready-success) ![Cloud](https://img.   shields.io/badge/Cloud-GCP-1A73E8)

## 📌 Executive Summary
The **Serverless Agentic Governance Controller (SAGC)** is an enterprise-grade reference architecture designed to solve a critical emerging business risk: **unbounded OpEx liability from autonomous AI workloads.** 

As agentic LLM loops scale, relying on application-level logic for budget control introduces severe risk of silent failures, race conditions, and prompt-injection-driven data exfiltration. SAGC decouples governance from business logic by implementing an out-of-process, fail-closed sidecar proxy mesh.

This repository serves as a blueprint for **Fiscal SecOps**, demonstrating how to enforce cryptographic identity, atomic budget tracking, and real-time semantic payload inspection without sacrificing developer velocity.

---

## 🏗️ Core Architectural Pillars

### 1. Fiscal SecOps & Atomic Distributed State
* **Linearizable Fencing Tokens:** Deprecated standard distributed caching (e.g., Redis Redlock) in favor of Google Cloud Spanner. Utilizes strict linearizable consistency and monotonically increasing fencing tokens to mathematically prevent split-brain double-spending during catastrophic regional failovers.
* **Token Burn Rate Limiters:** Hard network-layer drops (HTTP 429) execute before traffic reaches the internet if an agent exhausts its assigned Workload Identity budget.

### 2. Zero-Trust Data Plane
* **Strict mTLS & SPIFFE Binding:** Internal agent-to-gateway traffic is cryptographically authenticated. Open Policy Agent (OPA) strictly binds authorization to the Envoy-verified SPIFFE URI, rendering HTTP header spoofing impossible.
* **Default-Deny Egress:** Agent pods possess zero outbound internet access. All L7 LLM traffic is forcibly routed through the local Envoy sidecar via `ext_authz` gRPC interception.

### 3. Semantic Governance & Supply Chain Integrity
* **Unified Security Sidecar:** Outbound payloads are streamed locally via Envoy `ext_proc` to a localized ML container for PII redaction (Microsoft Presidio) and Prompt Injection Threat Detection.
* **Cryptographic ML Supply Chain:** To prevent dependency confusion and model-poisoning, all ONNX and NLP models are SHA-256 hashed, packaged as immutable OCI artifacts in Artifact Registry, and pinned via Kubernetes `InitContainers`.

### 4. Continuous Compliance & Runtime Defense
* **eBPF Kernel Monitoring:** CNCF Falco probes monitor container system calls, triggering critical alerts for zero-day RCE anomalies (e.g., spawned interactive shells) within the proxy containers.
* **Immutable WORM Audit Sinks:** All governance decisions are routed to Google Cloud Storage buckets locked under regulatory retention policies to guarantee forensic non-repudiation.

---

## 📖 Architectural Decision Records (ADRs)
This architecture was forged through rigorous, Staff-level adversarial Red Teaming. The evolution of the system, including acknowledged trade-offs and remediation of distributed systems vulnerabilities, is heavily documented in the `docs/adr/` directory.

**Key Reading:**
* `ADR 001`: Decoupling Fiscal Governance via Sidecar Proxy
* `ADR 024`: Internal Mutual TLS (mTLS) Mesh Infrastructure
* `ADR 031`: Deprecating Redlock for Linearizable Fencing Tokens
* `ADR 032`: ML Artifact Supply Chain Integrity

---

## ⚙️ Operational Status
This repository is configured for automated GitOps delivery via GitHub Actions. The CI/CD pipelines enforce Policy-as-Code (Rego syntax validation), Infrastructure-as-Code linting (`tfsec`), and strict Pod Security Standards (`kube-linter`) prior to deployment.
