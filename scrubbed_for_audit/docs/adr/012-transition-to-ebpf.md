# ADR 012: Transition to Sidecarless Governance (eBPF/Cilium)

## Status
Deferred

## Context
At 500+ agentic pods, the cumulative memory/CPU overhead of sidecar proxies (Envoy + OPA) in every pod introduces significant node-density tax. 

## Decision
We will transition to an **eBPF-based governance model** using Cilium.
* The budget check logic (Rego) will be compiled into eBPF bytecode.
* The Cilium Agent will enforce the budget check directly in the Linux Kernel, bypassing user-space network hops entirely.

## Consequences
* **Positive:** Near-zero overhead for policy enforcement; drastic reduction in memory footprint per pod.
* **Negative:** Increased complexity in debugging kernel-space logic; requires specialized Cilium/eBPF operational skills.
