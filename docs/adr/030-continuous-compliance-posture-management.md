# ADR 030: Continuous Compliance Posture Management (CSPM)

## Status
Accepted

## Context
Validating regulatory compliance (SOC2, ISO27001) manually is highly inefficient and creates significant "compliance drift" blind spots between formal audit cycles. The organization requires mathematically verifiable, real-time proof that our implemented architectural guardrails (WORM storage, default-deny egress, Identity Federation) remain active and uncompromised.

## Decision
We will implement a Continuous Compliance Posture Management (CSPM) platform (e.g., Google Cloud Security Command Center Premium or a third-party equivalent like Wiz/Prisma Cloud).
1. The CSPM will continuously ingest telemetry, IAM policies, and configuration states from the GCP Organization and GKE Autopilot clusters.
2. It will automatically map these live configurations to standardized compliance frameworks (e.g., NIST 800-53, SOC2 Type II).
3. Any configuration drift (e.g., a bucket losing its WORM lock, or an IAM binding bypassing the IdP) will trigger an immediate high-priority alert to the FinOps/SecOps pipeline.
4. The CSPM dashboard will serve as the primary, read-only system of record for external auditors to gather evidence.

## Consequences
* **Positive:** Automates audit evidence gathering; prevents silent compliance drift; provides real-time visibility into the infrastructure's regulatory posture.
* **Negative:** Enterprise CSPM tools introduce substantial licensing costs; requires aggressive baseline tuning to prevent false-positive alert fatigue for the SRE team.
