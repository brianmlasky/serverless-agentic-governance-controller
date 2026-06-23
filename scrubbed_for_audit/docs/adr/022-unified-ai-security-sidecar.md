# ADR 022: Unified AI Security Sidecar (DLP & Prompt Injection)

## Status
Accepted

## Context
Agentic workflows require protection against both data exfiltration (PII leakage) and semantic attacks (Prompt Injection/Jailbreaks). Implementing separate sidecars or inline API calls for each security check introduces unacceptable latency and architectural friction. 

## Decision
We implement a single, unified `ai-security-sidecar` deployed alongside the Envoy proxy in the SAGC Gateway pods.
1. Envoy intercepts outbound LLM requests and streams the payload to the sidecar via the `ext_proc` gRPC filter over `localhost`.
2. The sidecar executes a sequential semantic pipeline:
   - **Step 1 (DLP):** Identifies and masks sensitive entities.
   - **Step 2 (Threat Detection):** Evaluates the masked payload for adversarial prompt injection techniques.
3. If an attack is detected, the sidecar instructs Envoy to drop the request and return an `HTTP 403`. Otherwise, it returns the mutated, clean payload for routing.

## Consequences
* **Positive:** Centralizes semantic governance; minimizes network latency by keeping inspections local; abstracts complex NLP/ML security logic away from the core proxy and agent applications.
* **Negative:** Increases the CPU and memory footprint of the Gateway pod; the sidecar becomes a critical failure point (requires fail-closed logic if the sidecar crashes).
