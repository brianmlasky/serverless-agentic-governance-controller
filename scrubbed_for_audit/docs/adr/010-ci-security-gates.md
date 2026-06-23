# ADR 010: CI/CD Security & Policy Gates

## Status
Accepted

## Decision
The CI/CD pipeline is promoted to an authoritative **Security Gate**. No infrastructure or governance policy can be merged without passing:
1. **Rego Linting:** Syntactic validation of governance logic.
2. **Kube-Linter:** Enforcement of Pod Security Standards (no root, read-only FS).
3. **Policy Simulation:** Automated simulation of denial events to ensure Rego changes don't inadvertently "fail-open."

## Rationale
"Shifting left" on governance ensures that the SRE team never has to debug policy syntax errors in production. The pipeline is the first line of defense against both human error and malicious intent.
