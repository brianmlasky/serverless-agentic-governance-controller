---
name: Architectural Feature & Infrastructure Request
about: Propose a new platform feature, structural mutation, or agentic workload.
title: 'feat(arch): [Brief Description]'
labels: 'architecture, needs-triage'
assignees: ''
---

## 1. The Intention (The 'Why')
## 2. Architectural Lineage Check
- [ ] **ADR Required:** Does this change our compute, identity, or data storage paradigm? (If yes, draft an ADR first).
- [ ] **Design Spec Required:** Does this consume new IP space, define new SLIs, or alter IAM roles? (If yes, update the Specs).

## 3. Resilience & Blast Radius Analysis
* **IAM Boundary:** Which Workload Identity will this consume?
* **Network Boundary:** Does this require cross-VPC or external internet egress?
* **Fiscal Boundary:** What is the estimated cost impact, and what are the namespace resource limits?

## 4. Agentic Policy-as-Code Alignment
- [ ] Changes will be fully evaluated by `tfsec` and `tflint` in CI/CD.
- [ ] Target architecture adheres to the Threat Model (SAS 001).