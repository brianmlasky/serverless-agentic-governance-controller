# Policy Logic Document: Agentic Governance Controller (SAGC)

## 1. Purpose
This document defines the governance invariants enforced by the SAGC. The controller operates as a "Fiscal Circuit Breaker," ensuring that autonomous AI agents do not exceed predefined operational budgets or violate security posture during high-throughput inference tasks.

## 2. Fiscal Invariants (The "Hard" Constraints)
The following logic is enforced atomically at the middleware layer before any inference request reaches the model endpoint:

### Constraint 1: Maximum Token Burn Rate (MTBR)
* **Requirement:** Total cumulative token usage for a defined session must not exceed 10,000 tokens/minute.
* **Implementation:** The SAGC queries the `BudgetState` store. If `(SessionTokens + ProjectedTokens) > 10,000`, the request is rejected with a `403 Forbidden: Fiscal Limit Exceeded`.

### Constraint 2: Fail-Closed Default (Security Posture)
* **Requirement:** Any service degradation in the governance controller must result in a total stop of inference traffic.
* **Implementation:** The controller checks `HealthStatus` of the budget database. If the database is unreachable, the policy engine defaults to `allow = false`.

## 3. Traceability Logic (Mapping to Business Value)

| Business Rule | Policy ID | Enforcement Point | Success Metric |
| :--- | :--- | :--- | :--- |
| Prevent Budget Runaway | FISCAL_01 | Admission Control | < 0.1% drift from budget |
| Enforce Model Access | SEC_01 | Request Payload Inspection | 0 unauthorized inferences |
| Maintain System Integrity | OPS_01 | Health Check Loop | < 5ms latency impact |

## 4. Logic Decoupling Philosophy
Governance logic is explicitly decoupled from the agent's application code. The Agentic Controller uses **Rego** to evaluate the request context. This allows security and finance teams to update governance policies (e.g., lower the MTBR) via Git PRs without requiring a redeployment of the AI agent infrastructure.