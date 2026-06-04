## Architectural Standard: The Repository Pattern (Decoupling)

To prevent strict vendor lock-in and brittle codebases, all proprietary cloud SDK calls (e.g., `boto3` for AWS DynamoDB) must be wrapped in a Repository Interface.

*   **The Interface:** The application logic requests data via a generic method (e.g., `get_user_by_id(123)`).
*   **The Repository:** A dedicated layer executes the specific cloud-native query.
*   **The Result:** If the backend database changes (e.g., from DynamoDB to PostgreSQL), only the Repository file requires rewriting. The core application logic remains untouched, guaranteeing high code-reuse.

---

## Architectural Standard: Infrastructure Abstraction (Terraform Modules)

Do not write raw, hard-coded infrastructure configurations (e.g., a 50-line file defining a specific DynamoDB table).

*   **The Standard:** Wrap infrastructure in reusable Terraform Modules (e.g., a generic `data_store` module accepting `name` and `capacity` as variables).
*   **The Portability Advantage:** This abstraction hides the complexity of the specific cloud provider. If the platform migrates to GCP, developers do not rewrite the module; platform engineering simply provides a GCP-compatible version of the module.

---

## Internal Tooling Adoption Strategy

When rolling out new governance tools or controllers, mandates must be a last resort. Use the **Pilot Program Strategy**:

*   **Pilot:** Identify two high-performing teams experiencing the specific friction your tool solves. Treat them as design partners.
*   **Socialize:** Present the tool as a solution to manual toil, not as a compliance mandate.
*   **Empower:** Make the "secure path" the easiest path. Adoption should be driven by the fact that the tool saves developers time.

## Architectural Standard: Technical Debt Registry

Technical debt (temporary architectural trade-offs taken to meet business constraints) must be visible and managed.

*   **Location:** Tracked via specific labels (`technical-debt` or `architectural-risk`) in the primary issue tracker (Jira/GitHub Issues).
*   **Required Fields:** Every entry must contain:
    *   **Context:** Why the trade-off was made (e.g., MVP deadline).
    *   **Risk:** What breaks if left unfixed (e.g., 20% latency increase).
    *   **Repayment Plan:** What the architectural fix looks like.
*   **Governance:** 20% of sprint capacity is strictly reserved for "Debt Registry Maintenance."

---

## Framework Evaluation Checklist (The "Wrong Tool" Test)

Before adopting a new framework or technology, it must pass the following checks:

*   **Maintenance Test:** Who fixes the framework's bugs at 2 AM?
*   **Problem-Solution Fit:** Does it solve an existing bottleneck, or does it introduce new deployment complexities?
*   **Longevity Test:** Is the project backed by a foundation/enterprise, or a single maintainer?
*   **Operational Maturity:** Does it natively integrate with existing Terraform modules and telemetry stacks without custom "glue code"?
*   **Adoption Protocol:** Execute a two-day "Spike" (Proof-of-Concept) to validate business value before architectural inclusion.
