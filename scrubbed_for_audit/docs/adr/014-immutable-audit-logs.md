# ADR 014: Immutable Audit Log Integrity

## Status
Accepted

## Context
To achieve regulatory compliance (SOC2/GDPR) and provide forensic readiness, our audit logs must be immune to tampering, even by an administrative user.

## Decision
We automate the creation of the WORM (Write-Once-Read-Many) audit sink using Terraform.
1. Logs are routed to a GCS bucket with a 365-day retention policy.
2. The retention policy will be "Locked" via Terraform after the initial deployment phase to ensure non-repudiation.
3. This configuration is version-controlled and immutable, preventing configuration drift.

## Consequences
* **Positive:** Ensures forensic integrity; meets the most stringent audit requirements for "non-repudiation."
* **Negative:** Requires strict management of the storage bucket, as it cannot be deleted until the retention period expires.