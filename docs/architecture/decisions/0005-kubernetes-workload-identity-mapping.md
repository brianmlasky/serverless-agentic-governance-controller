# ADR 0005: Kubernetes Workload Identity Mapping and Resource Governance

## Status
Accepted

## Context
The Serverless Agentic Governance Controller must execute within a GKE cluster (`agentic` namespace) and securely authenticate to Google Cloud APIs (Secret Manager) without mounting static JSON credentials. Furthermore, as an autonomous agentic workload, it presents a risk of runaway compute consumption if not strictly governed.

## Decision Outcome
1. **Identity:** We implement Kubernetes Workload Identity Federation. The `sagc-agent-sa` Kubernetes Service Account is annotated with `iam.gke.io/gcp-service-account`, securely bridging the namespace boundary to GCP IAM.
2. **Fiscal SecOps:** The deployment manifesto enforces strict CPU and Memory requests/limits, establishing a hard compute ceiling that mathematically bounds the maximum operational cost of the pod.
