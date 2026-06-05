# ADR 004: GitOps Terraform Pipeline Execution and Governance

**Date:** 2026-06-05
**Status:** Approved
**Context:** Following the migration of our infrastructure state to a secure GCS backend (ADR 003), the execution phase of our Terraform deployments remains tied to localized, manual terminal environments. This represents a single point of failure, introduces configuration drift, and bypasses the audit and compliance requirements necessary for regulatory-grade incident investigations and strict Fiscal SecOps.

**Decision:** We mandate the deprecation of local `terraform apply` executions. All infrastructure mutations will be handled exclusively by an automated GitOps pipeline via GitHub Actions, serving as the single source of truth for the platform state.

### Business & Operational Justification
* **Auditable Velocity:** The version control system becomes an immutable audit log. Every infrastructure change is tracked by author, reviewer, timestamp, and pipeline execution output.
* **Peer Enablement:** The barrier to entry for platform contribution is minimized. Peers do not require local Terraform installations or highly privileged GCP credentials; they only need to submit a Pull Request.
* **Fiscal SecOps:** Manual terminal execution is the leading cause of anomalous cloud spend. Gating deployments behind a peer-reviewed automation pipeline systematically reduces catastrophic provisioning errors.

### Trade-Offs
* Intentional friction introduced into the iteration loop (waiting for CI runners vs. instant local feedback).
* Overhead required to maintain the CI/CD YAML definitions.
* Troubleshooting moves from local CLI context to remote CI pipeline logs.

### Security & Compliance Guardrails

**1. Blast Radius Containment**
The pipeline will authenticate via Workload Identity Federation (WIF). The WIF service account is strictly scoped via IAM to the specific target project and GKE cluster boundaries, explicitly denying lateral movement across the broader GCP organization.

**2. Disaster Recovery & Emergency Intervention**
* **Standard Rollback:** Revert the offending Pull Request in GitHub and allow the pipeline to automatically reconcile the state.
* **Break-Glass Protocol:** In the event of a pipeline failure during a Sev-1 outage, designated personnel may use Privileged Access Manager (PAM) or Vault to temporarily access the GCP UI/CLI. All UI mutations must be backported into the Terraform code during the mandatory incident post-mortem to resolve drift.

**3. Separation of Duties (SoD)**
Branch protection rules are enforced on the `main` branch. A minimum of one approving review from a peer is required before merge. The author of the code cannot unilaterally execute the pipeline, mathematically enforcing SoD for regulatory compliance.

**4. Policy-as-Code Pre-Flight Checks**
To guarantee Fiscal SecOps and security boundaries are respected, the Pull Request stage will integrate automated tooling (e.g., `tfsec` for vulnerability scanning and `Infracost` for budget analysis). The PR will automatically fail validation if the code violates established cost-center or security policies before reaching the execution phase.
