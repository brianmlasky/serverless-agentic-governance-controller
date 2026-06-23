## Architectural Lineage (The Three-Gate Rule)
* **Intention Gate:** Resolves / Implements ADR # [Insert ADR ID]
* **Boundary Gate:** Adheres to Design Spec # [Insert Spec ID]

## Description of Changes
## Security & Blast Radius Check
- [ ] IAM privileges are tightly scoped (Least Privilege applied).
- [ ] No public IP addresses or exposed attack surfaces introduced.
- [ ] Changes adhere to the Threat Model (SAS).

## Agentic & Automated Peer Review Sign-Off
- [ ] Automated Policy-as-Code gates successfully passed (tflint, tfsec).
- [ ] Terraform plan output explicitly verified against Design Spec compute/IP limits.
- [ ] AI/Agentic Architectural Review completed; no outstanding security or blast-radius violations.