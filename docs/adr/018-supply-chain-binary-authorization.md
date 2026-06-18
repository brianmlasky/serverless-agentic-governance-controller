# ADR 018: Supply Chain Security via Container Image Signing

## Status
Accepted

## Context
Malicious actors frequently target CI/CD pipelines or container registries to inject compromised code into production workloads. If an attacker gains access to our Google Artifact Registry, they could overwrite or upload a poisoned container image that bypasses standard deployment checks.

## Decision
We enforce a strict cryptographic chain of custody for all production workloads:
1. **Cosign Image Signing:** All Docker images built via GitHub Actions will be cryptographically signed using Cosign (Sigstore) before being pushed to Google Artifact Registry.
2. **Binary Authorization:** We will enable Google Cloud Binary Authorization on our GKE Autopilot cluster.
3. **Admission Enforcement:** GKE will utilize an evaluation policy that blocks the deployment of any pod if its container image lacks a valid signature from our trusted CI/CD public key.

## Consequences
* **Positive:** Complete protection against tampered images or unauthorized registry uploads; ensures only validated code executes.
* **Negative:** Introduces key management complexity; pipeline disruptions (e.g., expired keys or failed signing steps) will cause immediate deployment blockages.
