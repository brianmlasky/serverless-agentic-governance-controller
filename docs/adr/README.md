# Architecture Decision Records (ADRs)

This directory contains the historical record of structural and fiscal decisions made for the `serverless-agentic-governance-controller` platform. 

## ADR Categorization Standard
When submitting a new ADR for review, it must adhere to one of the following two scopes:

1.  **CTO-Level ADRs (Technical Architecture)**
    * **Focus:** Business Alignment, Velocity, and Technical Risk mitigation.
    * **Example:** Deciding between Terraform vs. Pulumi for infrastructure provisioning based on team velocity and state management risk.
2.  **Accounting/Fiscal ADRs (Fiscal SecOps)**
    * **Focus:** Cost attribution, unit economics, and governance thresholds.
    * **Example:** Defining the maximum allowable token-burn rate for an AI agent before triggering an automated circuit breaker.
