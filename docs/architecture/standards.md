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
