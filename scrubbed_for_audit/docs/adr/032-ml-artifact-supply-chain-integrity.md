# ADR 032: ML Artifact Supply Chain Integrity

## Status
Accepted

## Context
ADR 018 established Binary Authorization for our container images. However, a Red Team audit revealed that our security sidecars (ADR 023) download ONNX threat models and spaCy NLP datasets dynamically at runtime. This bypasses the container signature, allowing a supply chain attacker to inject a poisoned model that silently disables threat detection or exfiltrates PII.

## Decision
We extend our cryptographic supply chain perimeter to include all ML artifacts.
1. Dynamic runtime downloading of ML models via the public internet (e.g., `pip` or HuggingFace hub) is strictly prohibited in the production cluster.
2. All required `.onnx` and NLP models will be downloaded securely during the CI/CD build phase.
3. Their SHA-256 digests will be calculated and pinned. The models will be packaged directly into a hardened, immutable OCI artifact and pushed to our private Google Artifact Registry.
4. A Kubernetes `InitContainer` will verify the SHA-256 hash of the mounted model volumes against a trusted ConfigMap before allowing the main security sidecar to start.

## Consequences
* **Positive:** Closes a critical data-exfiltration and logic-bypass vulnerability; ensures complete cryptographic integrity of the semantic evaluation pipeline.
* **Negative:** Increases the size of our deployment artifacts and the complexity of the CI/CD build pipeline.
