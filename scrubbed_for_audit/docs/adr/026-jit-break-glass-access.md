# ADR 026: Zero Standing Privileges and Just-In-Time (JIT) Access

## Status
Accepted

## Context
While the workload identities and network perimeters are heavily restricted, human administrators currently possess standing, highly privileged roles (e.g., `cluster-admin`, `roles/owner`). Compromise of an administrator's workstation would grant an attacker unrestricted ability to bypass all SAGC fiscal and security guardrails.

## Decision
We mandate Zero Standing Privileges (ZSP) for all human operators interacting with the production environment.
1. All persistent, highly privileged IAM roles assigned to human user accounts will be revoked.
2. We will implement a Just-In-Time (JIT) access broker (e.g., Google Cloud Privileged Access Manager or HashiCorp Boundary).
3. Engineers requiring production access must request a time-bound, cryptographically signed token (max duration: 2 hours) accompanied by a valid Jira/ITSM ticket number.
4. "Break-glass" emergency access will automatically trigger a PagerDuty alert to the security team and initiate heightened audit logging.

## Consequences
* **Positive:** Drastically reduces the blast radius of credential theft; ensures human access is ephemeral, audited, and tied to documented change management.
* **Negative:** Introduces friction to the developer experience; requires SREs to authenticate through an access broker during high-stress incident response scenarios.
