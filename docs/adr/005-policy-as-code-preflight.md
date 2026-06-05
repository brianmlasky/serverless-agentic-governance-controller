# ADR 005: Policy-as-Code and Automated Pre-Flight Checks

**Date:** 2026-06-05
**Status:** Approved
**Context:** Following the establishment of our automated GitOps pipeline (ADR 004), we must ensure that all infrastructure mutations comply with organizational security standards, Fiscal SecOps boundaries, and provider best practices *before* reaching the `terraform plan` or `apply` phases. Relying solely on manual peer review for complex HCL syntax and security vulnerabilities introduces unacceptable human error and operational bottlenecks.

**Decision:** We mandate the integration of a dual-layered, automated pre-flight gating system within the GitOps pipeline:
1. **TFLint:** For infrastructure syntax, deprecated instance type detection, and cloud-provider best practices.
2. **tfsec:** For static security analysis, ensuring resources are not provisioned with known vulnerabilities or compliance violations (e.g., unencrypted buckets, open firewalls).

### Consequences & Guardrails
* **Shift-Left Security:** Vulnerabilities and bad practices will hard-fail the CI/CD pipeline immediately, explicitly blocking the Pull Request from being merged.
* **Operational Empathy:** Reviewers are freed from auditing syntax and basic security checklists, allowing them to focus strictly on architectural logic and business intent.
* **Standardization:** Future maintainers inherit a system that automatically enforces its own coding and security standards, preventing architectural degradation over time.