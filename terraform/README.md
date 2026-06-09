# Operational Infrastructure Blueprint

This directory manages the core infrastructure layer for the Serverless Agentic Governance Controller.

## Zero-Trust Identity Mapping

| External Identity Provider | GCP Workload Identity Pool | Target GCP Service Account |
| :--- | :--- | :--- |
| **GitHub Actions** <br>`brianmlasky/serverless-agentic-governance-controller` | `sagc-pool` | `sagc-controller@alert-hall-466720-c0.iam.gserviceaccount.com` |
| **GKE Workload Identity** <br>Namespace: `agentic` <br>K8s SA: `sagc-agent-sa` | `sagc-pool` | `sagc-controller@alert-hall-466720-c0.iam.gserviceaccount.com` |

## Production Resource Identifiers
* **GCP Project Number:** `390958881559`
* **Fully Qualified Workload Provider URI:** `projects/390958881559/locations/global/workloadIdentityPools/sagc-pool/providers/github-actions`
