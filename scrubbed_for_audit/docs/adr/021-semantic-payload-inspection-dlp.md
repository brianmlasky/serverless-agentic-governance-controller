# ADR 021: Semantic Payload Inspection via Envoy Sidecar (DLP)

## Status
Accepted

## Context
If an internal agent inadvertently includes Personally Identifiable Information (PII) or restricted intellectual property in a prompt, that data will be transmitted to external providers, violating data privacy regulations. Relying on application-level logic to redact this data breaks the separation of concerns.

## Decision
We will implement Data Loss Prevention (DLP) natively within the Envoy Sidecar Proxy layer.
1. A Microsoft Presidio NLP container will be deployed as a sidecar alongside the Envoy proxy in the SAGC Gateway pods.
2. Envoy will utilize the `ext_proc` (External Processing) filter to stream all outbound HTTP request bodies to the local Presidio sidecar over a gRPC connection on `localhost`.
3. Presidio will mutate the payload, redacting sensitive entities (e.g., replacing a name with `[REDACTED_PERSON]`) before returning the mutated body to Envoy for external routing.

## Consequences
* **Positive:** Strict separation of security from application logic; impossible for agents to bypass redaction; near-zero latency due to local memory communication.
* **Negative:** Increases the memory footprint of the Gateway pods (requiring ~500MB additional RAM per pod to load the Presidio spaCy NLP models); requires complex Envoy filter configuration to safely parse dynamic LLM JSON schemas.
