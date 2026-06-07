# Design Specification 002: GKE Autopilot Compute Topology

## 1. Network Topology & IP Address Allocation
To avoid future routing collisions across multi-cloud and hybrid network topologies, the `sagc-cluster` utilizes a non-overlapping, VPC-native IP architecture localized to `us-central1`.

| Resource / Subnet Component | Purpose | CIDR Block | Max Allocation |
| :--- | :--- | :--- | :--- |
| `sagc-gke-subnet` (Primary) | GKE Node IP Allocation | `10.0.1.0/24` | 254 Nodes |
| `gke-pods` (Secondary) | Pod IP Address Space | `10.4.0.0/14` | 262,144 Pods |
| `gke-services` (Secondary) | Cluster Internal Services | `10.8.0.0/20` | 4,096 Services |
| `master_ipv4_cidr_block` | Managed GKE Control Plane | `172.16.0.0/28` | Enclosed /28 |

## 2. Blast Radius & IAM Isolation
Administrative access to the cluster control plane is governed by Google Cloud IAM, separating the control plane from the operational workload layer:
* **Infrastructure Management:** Bound to the GitHub Actions CI/CD Workload Identity Federation role. Direct human mutations are blocked.
* **Workload Identity:** Workloads (such as the LiteLLM proxy) will not use broad GCP service account keys. They will leverage GKE Workload Identity to assume scoped IAM roles dynamically.

## 3. Fiscal Governance Guardrails
To prevent unbounded scaling risks inherent to automated agentic platforms:
* **Resource Quotas:** Standard namespaces (`default`, `production`) will enforce explicit `ResourceQuota` limits via Kubernetes manifests to bound maximum concurrent vCPU and Memory footprints.
* **Release Boundary:** The cluster is bound to the `REGULAR` release channel to guarantee zero-touch security patching of the underlying node OS and control plane components.