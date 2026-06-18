# ADR 013: Vault-Native & Workload Identity Shift

## Status
Accepted

## Context
Following the identification of static service account keys in the repository, we are moving to a "Zero-Secret-in-Git" architecture.

## Decision
1. **Workload Identity:** We will migrate all infrastructure provisioning (Terraform) and application workloads to use Google Cloud Workload Identity. This binds Kubernetes Service Accounts to IAM roles, eliminating the need for static `key.json` files.
2. **External Secrets:** Non-GCP secrets (e.g., Database URLs, API keys) will be fetched at runtime via the `external-secrets-operator` from HashiCorp Vault.
3. **Prevention:** We add `gitleaks` as a mandatory pre-commit hook to block any future commits containing sensitive key patterns.

## Consequences
* **Positive:** Credentials are ephemeral and never stored in version control; attack surface is reduced to zero for static keys.
* **Negative:** Requires initial configuration overhead to bind KSA identities to IAM roles.
