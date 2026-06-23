# ADR-044: FinOps Constraints on WORM (Write Once, Read Many) Compliance

## Status
Accepted

## Context
The SAGC architecture utilizes Google Cloud Storage with a `storage.objectCreator` IAM binding to enforce an immutable audit trail for governance decisions. To achieve strict regulatory WORM compliance, the bucket requires a locked retention policy. However, locking a GCP retention policy is physically irreversible for the duration of the hold (e.g., 5 years). 

## Decision
For this reference architecture and non-production environments, we will implement the IAM isolation layer but **intentionally forego the hard infrastructure retention lock**. 

## Consequences
- **Positive (FinOps):** Prevents the catastrophic financial risk of a runaway logging loop creating an undeletable, unbounded OpEx liability for the next 5 years.
- **Negative (Security):** Leaves a theoretical vulnerability where an adversary with `storage.bucketAdmin` privileges could modify the bucket lifecycle policies to destroy evidence.
- **Mitigation:** In a true Tier-0 production deployment, the FinOps risk is accepted by the business, and the `--lock-retention-policy` flag must be enforced via Terraform.