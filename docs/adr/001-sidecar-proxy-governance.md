# ADR 001: Decoupling Fiscal Governance via Sidecar Proxy Pattern

**Date:** 2026-06-05
**Status:** Accepted

## Context
As the organization scales autonomous AI workloads, the risk of "runaway agents" (infinite reasoning loops) causing severe budget exhaustion increases. We need a mechanism to enforce strict fiscal limits (Token Burn Rate) on these agents. 

Initially, the proposal was to integrate a budget-checking library directly into the application code of every AI agent (e.g., importing a Python SDK to check the budget before every LLM call). 

## Decision
We will reject the direct-integration approach and instead implement the Serverless Agentic Governance Controller (SAGC) as an out-of-process **Sidecar Proxy** (Admission Control Middleware) deployed within the same Kubernetes Pod as the AI workload. All outbound egress traffic to LLM providers will be forcibly routed through this sidecar via `iptables` interception.

## Rationale (The "Why")
1. **Language Agnostic Portability:** By intercepting traffic at the network layer (L7), the governance controller works universally. We can deploy AI agents written in Python, Rust, or Go without needing to maintain separate budget-checking SDKs for each language.
2. **Immutability of Governance:** Developers cannot accidentally (or maliciously) bypass the budget checks by modifying their application code or failing to invoke the library. The network-level interception guarantees compliance.
3. **Forensic Preservation:** In the event of a budget exhaustion (Circuit Breaker trip), the sidecar can sever outbound API traffic while leaving the AI Agent pod in a `Running` state. This preserves local memory and OpenTelemetry trace spans, allowing for a regulatory-grade post-mortem investigation into the hallucination loop.

## Consequences
* **Positive:** Complete decoupling of business logic (the AI Agent) from governance logic (the SAGC). Security and platform teams can update fiscal policies without requiring the AI engineering teams to redeploy their code.
* **Negative (Trade-off):** Introduces a minor latency penalty (approx. 2-5ms) to every outbound LLM request due to the extra network hop inside the pod. Given the high latency of LLM generation itself, this overhead is deemed an acceptable trade-off for strict fiscal security.
