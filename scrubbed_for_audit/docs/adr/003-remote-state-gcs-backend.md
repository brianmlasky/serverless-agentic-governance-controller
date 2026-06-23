# ADR 003: Remote State Management via GCS Backend

**Date:** 2026-06-05
**Status:** Approved
**Context:** The deployment architecture for the `serverless-agentic-governance-controller` ecosystem requires decoupling the infrastructure state from transient local container runtimes (e.g., GitHub Codespaces). Storing state locally introduces single points of failure, concurrency race conditions, and completely blocks CI/CD capability for infrastructure automation.

**Decision:** We mandate migrating the Terraform state storage mechanism from the standard local file state driver to a remote, highly available **Google Cloud Storage (GCS)** backend.

### Architecture
* **State Sync:** Terraform CLI (Local/CI) communicates with the GCS State Bucket via TLS 1.3.
* **Storage:** Encrypted and locked GCS bucket specifically dedicated to state management.

### Consequences & Guardrails
1.  **State Locking:** GCS natively handles lock operations via object holds, preventing corruption from concurrent execution runs across distributed operations teams or automated pipelines.
2.  **Access Control:** Access to infrastructure state secrets is completely decoupled from repository read permissions, restricted strictly via granular Cloud IAM controls.
3.  **Operational Readiness:** This structural change satisfies the prerequisites for migrating to an automated pipeline execution model (GitOps) via GitHub Actions runner workloads.
