# ADR 023: Security Sidecar Inference Engines

## Status
Accepted

## Context
ADR 022 established the architectural pattern of a Unified AI Security Sidecar. We must now define the specific evaluation engines utilized within that sidecar to balance latency, operational cost, and security efficacy.

## Decision
We select the following engines for local sidecar evaluation:
1. **DLP Engine:** Microsoft Presidio. We favor its hybrid approach (Regex + spaCy NLP) to drastically reduce false positives compared to pure regex, accepting the ~500MB memory overhead.
2. **Threat Detection Engine:** Local Quantized ML Model (e.g., `deberta-v3` via ONNX). We explicitly reject external API-based threat detection to prevent double network latency, avoid third-party API costs, and maintain strict data sovereignty over our raw prompts.

## Consequences
* **Positive:** Achieves near-zero network latency for critical security checks; eliminates recurring API costs for security scanning; ensures raw payloads do not leave the VPC for governance evaluation.
* **Negative:** The GKE Autopilot pods will require significantly higher memory requests to load both the Presidio NLP models and the ONNX threat models into local RAM.
