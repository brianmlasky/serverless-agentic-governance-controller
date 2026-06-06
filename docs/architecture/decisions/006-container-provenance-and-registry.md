# ADR 006: Immutable Container Provenance via Google Artifact Registry

## Status
Accepted

## Context
The Serverless Agentic Governance Controller requires a secure, high-availability container registry to host proxy images (e.g., LiteLLM) and bespoke agentic workloads. Relying on public registries (like Docker Hub) introduces severe supply chain vulnerabilities, rate-limiting risks, and untracked network egress costs. Furthermore, in an Agentic SecOps paradigm, container images must be treated as immutable artifacts; allowing an image tag to be overwritten introduces the risk of silent workload regressions or malicious proxy injections.

## Decision
We will provision Google Artifact Registry (GAR) as the exclusive container provenance authority for this platform. 
1. **Locality:** The registry will be localized to the `us-central1` region, co-located with the GKE control plane to eliminate cross-region egress costs.
2. **Immutability:** We will strictly enforce immutable image tags. Once a digest is associated with a tag (e.g., `v1.2.0`), it cannot be overwritten.
3. **Format:** Docker standard format to natively support Kubernetes pod specifications.

## Consequences
* **Positive:** Complete mitigation of Docker Hub rate limits.
* **Positive:** Enforcement of immutable tags protects against container tampering.
* **Positive:** Deep IAM WIF integration ensures only our specific GitHub Actions deployer identity can write images to this registry.
* **Negative:** Introduces a marginal, predictable storage cost for retained images, requiring periodic lifecycle management policies to purge deprecated digests.