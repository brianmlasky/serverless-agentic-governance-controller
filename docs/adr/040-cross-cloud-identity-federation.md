# ADR 040: Cross-Cloud Identity Federation (Zero-Trust)

**Status:** Accepted
**Date:** 2026-06-23

## Context and Problem Statement
The Serverless Agentic Governance Controller operates within a Google Cloud Platform (GKE) environment but routes traffic to LLM providers across multiple clouds, including AWS Bedrock. Storing long-lived static AWS API keys in GCP secrets introduces a massive security risk, violating Zero-Trust principles and creating secret rotation overhead. How do we securely authenticate across cloud boundaries?

## Decision
We will implement an Active-Passive Multi-Cloud Disaster Recovery posture using short-lived Identity Federation. We explicitly reject the use of static IAM user credentials.

1. **GCP Identity Provisioning:** The gateway pod runs under a dedicated Kubernetes ServiceAccount (`litellm-wif-sa`) bound to a Google Cloud IAM Service Account via Workload Identity Federation (WIF).
2. **AWS OIDC Trust:** We utilize an AWS IAM OpenID Connect (OIDC) Provider that explicitly trusts the GCP cluster's issuer URL (`container.googleapis.com/...`).
3. **Least-Privilege Assume Role:** The AWS IAM Role (`dev-litellm-bedrock-role`) enforces a strict trust policy condition. It validates the cryptographic subject (`sub`) of the incoming token, ensuring *only* the specific `agentic` namespace and ServiceAccount can invoke the `sts:AssumeRoleWithWebIdentity` action.

## Consequences
* **Positive:** Cryptographically secure, secretless cross-cloud routing. If the GCP cluster is compromised, the attacker cannot extract a static AWS key. 
* **Positive:** Structurally validates our multi-cloud governance capability for enterprise environments.
* **Negative:** Introduces complexity in local debugging, as the full GCP Workload Identity token chain must be present or explicitly mocked to test AWS Bedrock routing.