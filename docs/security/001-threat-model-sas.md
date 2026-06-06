# SAS 001: Threat Model & Security Architecture

## 1. Trust Boundaries
* **External (Untrusted):** Any traffic originating outside the `sagc-vpc`.
* **Internal (Zero-Trust):** East-West traffic between Pods within the GKE cluster. We operate on an assumed-breach model; internal traffic must be authenticated.
* **Management Plane (Highly Restricted):** Access to the GCP APIs and GCS Terraform state. Restricted strictly to GitHub Actions Workload Identity Federation (WIF).

## 2. STRIDE Threat Mitigation Analysis
| Threat Category | Platform Mitigation Strategy |
| :--- | :--- |
| **Spoofing** | GitHub Actions WIF eliminates static credentials. GKE Workload Identity maps Kubernetes Service Accounts to GCP IAM without exporting keys. |
| **Tampering** | Artifact Registry explicitly configured for `immutable_tags = true`. Terraform state locked in GCS. |
| **Information Disclosure** | VPC-native GKE cluster with `enable_private_nodes = true`. No public IP routing to compute instances. |

## 3. Data Classification
* **Secret Data:** API Keys for target LLMs. Stored strictly in Google Secret Manager, injected at runtime into the LiteLLM pods via Workload Identity.