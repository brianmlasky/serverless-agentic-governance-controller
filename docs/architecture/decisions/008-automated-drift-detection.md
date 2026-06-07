# ADR 008: Automated Infrastructure Drift Detection

## Status
Accepted

## Context
As the Serverless Agentic Governance Controller scales, the risk of "ClickOps" (manual mutations in the GCP Console) or out-of-band API calls increases. If the real-world state of Google Cloud drifts from the declarative state stored in GitHub, our disaster recovery capabilities are compromised, and security vulnerabilities can be silently introduced.

## Decision
We will implement an automated Drift Detection pipeline using GitHub Actions.
1. A CRON job will execute a `terraform plan` against the production environment every 12 hours.
2. The pipeline will utilize Terraform's `-detailed-exitcode` flag. If the plan detects that infrastructure must be created, updated, or destroyed to match the Git state, the pipeline will purposefully fail.
3. A pipeline failure serves as a P1 alert that unauthorized or untracked infrastructure changes have occurred in the cloud environment.

## Consequences
* **Positive:** Mathematically guarantees that the `main` branch is the absolute source of truth.
* **Positive:** Immediately detects and alerts on manual security group or IAM bypasses.
* **Negative:** Requires strict discipline; emergency hotfixes made in the GCP console will trigger pipeline failures until backported into Terraform.