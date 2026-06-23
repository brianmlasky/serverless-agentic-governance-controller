# CONTRIBUTING.md
To add a new guardrail: 1) Draft policy in `k8s/policies/sidecar/`. 2) Simulate with `opa eval`. 3) PR to main. The CI pipeline will automatically run security gates. Approval from both Platform and FinOps is required.
