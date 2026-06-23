# ADR 0004: Mandatory Review Gates via CODEOWNERS

## Status
Accepted

## Context
As the platform scales and more engineers contribute, the risk of accidental configuration drift in critical control planes (CI/CD pipelines, IAM bindings, Terraform state) increases. Informal agreements to "always review Terraform" do not survive organizational friction. 

## Decision Outcome
We have implemented a `.github/CODEOWNERS` boundary.

By mapping critical directories (`/terraform/`, `/.github/workflows/`, `/docs/architecture/`) to specific Principal Architects, the version control system natively enforces a hard blocker on Pull Requests modifying these paths. 

### Positive Consequences
* Governance is enforced by the system, not by human memory.
* Junior engineers can experiment safely in feature branches, knowing the system will prevent them from merging destructive infrastructure changes without senior oversight.
* The architectural ledger (`docs/architecture/decisions/`) is protected from unauthorized historical revisionism.
