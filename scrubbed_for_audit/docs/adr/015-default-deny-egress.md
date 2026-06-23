# ADR 015: Default-Deny Egress Architecture

## Status
Accepted

## Context
Autonomous AI agents are highly susceptible to prompt injection. If an agent is compromised, it may attempt to exfiltrate data or establish command-and-control (C2) connections to unauthorized external domains. Kubernetes defaults to allowing all egress traffic.

## Decision
We implement a **Zero-Trust Default-Deny Egress Network Policy** across the workload namespace.
1. All outbound traffic from agent pods is dropped at the network layer.
2. Egress is explicitly allowed *only* to the internal SAGC API Gateway.
3. The API Gateway is explicitly allowed to egress *only* to approved LLM provider endpoints (e.g., OpenAI, Anthropic, GCP Vertex) via FQDN/IP whitelisting.

## Consequences
* **Positive:** Mathematically prevents unauthorized data exfiltration and "Shadow IT" external API calls.
* **Negative:** Adding new external tools or APIs requires an infrastructure code change to update the allowed egress list.
