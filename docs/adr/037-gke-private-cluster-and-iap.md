# ADR 037: Zero-Trust Control Plane Isolation via Cloud IAP

## Status
Accepted

## Context
During the deployment of the Serverless Agentic Governance Controller (SAGC), local execution of chaos testing scripts against the GKE Autopilot cluster resulted in HTTP 503 Service Unavailable errors and TCP connection timeouts (`dial tcp ... i/o timeout`). Investigation revealed that the local development environment was attempting to route administrative `kubectl` traffic over the public internet to a hardened, private cluster control plane. Furthermore, manual VPC peering modifications caused severe Terraform state drift (`Error 409: Requested entity already exists`), undermining our Infrastructure-as-Code (IaC) immutability guarantees.

## Decision
To enforce a strict Zero-Trust security posture while maintaining IaC parity, we mandate the following networking architecture:

1.  **Private-Only Control Plane:** The GKE Autopilot cluster must be provisioned without a public endpoint. Master authorized networks are strictly prohibited from utilizing public IP whitelists.
2.  **Identity-Aware Proxy (IAP) Tunneling:** All administrative access (`kubectl`, chaos testing scripts) originating from outside the VPC must be routed through a Cloud IAP TCP forwarding tunnel bound to `localhost`. Access is governed strictly by the `roles/iap.tunnelResourceAccessor` IAM binding rather than network-level allowlists.
3.  **Explicit VPC Peering Declarations:** Terraform must explicitly manage the `google_compute_global_address` and `google_service_networking_connection` resources for Private Service Access. Implicit creation via `gcloud` or the GCP Console is prohibited to prevent state drift.

## Consequences
* **Positive:** Cryptographically verified, identity-based access to the cluster control plane via Google's backbone, eliminating public attack surfaces.
* **Positive:** Absolute state synchronization between GCP infrastructure and the Terraform state file.
* **Negative/Constraint:** Introduces local development friction; engineers must explicitly initialize and authenticate an IAP tunnel before interacting with the cluster API.