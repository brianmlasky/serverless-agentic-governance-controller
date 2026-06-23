# ADR 001: Decoupling Fiscal Governance via Sidecar Proxy

**Date:** 2026-06-05
**Status:** Accepted
**Primary Business Driver:** Protect organizational OpEx (budget) from infinite AI reasoning loops without sacrificing developer velocity.

## Context
As we scale autonomous AI workloads, the business requires a hard fiscal circuit breaker. The architectural challenge is enforcing strict "Token Burn Rate" limits without forcing our data science and engineering teams to rewrite their agents or learn complex governance libraries. 

## Decision
We will implement the Serverless Agentic Governance Controller (SAGC) as an out-of-process **Sidecar Proxy**. All outbound egress traffic to LLM providers will be forcibly routed through this sidecar via network-layer interception.

## Considered Alternatives
1.  **Application-Level SDK (Rejected):** Forcing developers to import a budget-checking library. *Why rejected:* High developer friction. Vulnerable to accidental bypass if a developer forgets to invoke the library. Not language-agnostic.
2.  **Full Service Mesh e.g., Istio/Linkerd (Rejected):** Deploying a global service mesh for L7 traffic management. *Why rejected:* Massive operational tax and complexity. We currently only require outbound API governance, making a full mesh an over-engineered "sledgehammer" that violates our complexity budget.
3.  **Serverless API Gateway (Rejected):** Routing all agents through a centralized cloud gateway. *Why rejected:* Introduces a single global point of failure and potential latency bottlenecks for internal cluster traffic.

## Rationale
* **Immutability of Governance:** Network-level interception guarantees compliance. Agents cannot bypass the budget check, ensuring the business is protected from runaway costs.
* **Forensic Preservation:** In the event of budget exhaustion, the sidecar drops the outbound network packet (returning HTTP 429) but leaves the AI Agent pod running. This preserves local memory and trace spans for root-cause analysis.

## Consequences (Trade-offs)
* **Positive:** Complete decoupling of business logic from governance. Security teams can update fiscal policies without AI teams redeploying code.
* **Negative:** Introduces a minor latency penalty (2-5ms) to every outbound LLM request due to the extra localhost network hop. 

## Future Considerations (Deferred Decisions)
* As the cluster scales beyond 500+ agentic pods, the resource overhead of running a sidecar in every pod may become inefficient. At that scale, we will defer the decision to evaluate eBPF (Sidecarless) mesh technologies like Cilium to push these network policies directly to the Linux kernel level.
