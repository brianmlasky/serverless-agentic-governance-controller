# ADR 029: Enterprise Identity Federation (SAML/OIDC)

## Status
Accepted

## Context
Currently, access to the SAGC environment (via Cloud IAP or Kubernetes RBAC) relies on isolated Google Cloud identities. This creates a fragmented identity perimeter that is disconnected from the enterprise HR lifecycle (onboarding, role changes, terminations), risking lingering access for offboarded personnel.

## Decision
We mandate Enterprise Identity Federation for all human interaction with the system.
1. Google Cloud Identity will be federated with the corporate Identity Provider (IdP) — such as Okta or Azure AD — using SAML 2.0 or OIDC.
2. Direct user-level IAM bindings in GCP will be strictly prohibited. All access must be granted via IdP-managed groups (e.g., `SAGC-Admins`, `SAGC-Viewers`).
3. Kubernetes Role-Based Access Control (RBAC) will utilize OIDC tokens issued by the central IdP, mapping cluster permissions directly to corporate group claims.

## Consequences
* **Positive:** Ensures compliance with automated offboarding requirements; centralized audit logging for all authentication events; enforces corporate MFA policies globally.
* **Negative:** Creates a hard dependency on the external IdP; an outage in Okta/Azure AD will completely lock out all human administrators from the GCP environment and GKE clusters.
