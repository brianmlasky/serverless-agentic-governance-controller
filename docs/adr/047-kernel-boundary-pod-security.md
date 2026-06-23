# ADR-047: Kernel Boundary Hardening and Pod Security Standards

## Status
Accepted

## Context
An adversarial architecture audit highlighted several critical vulnerabilities assuming a porous container boundary: Envoy sidecar socket hijacking (SPIFFE spoofing), Workload Identity token leakage, and memory exhaustion leading to cascading node failures. 

## Decision
All agentic workloads operating within the SAGC mesh must adhere to strict Kubernetes Pod Security Standards (Restricted profile). This includes `readOnlyRootFilesystem: true`, dropping all Linux capabilities (`capabilities.drop: ALL`), and enforcing strict CPU/Memory limits.

## Consequences
- **Positive (Security):** Mathematically restricts the blast radius of a compromised agent loop. The attacker cannot write to the filesystem, hijack Envoy's Unix sockets, or execute kernel-level container escapes.
- **Positive (Resilience):** Hard memory limits prevent a hijacked agent from flooding the Envoy `ext_proc` buffer to the point of a node-level Out-of-Memory (OOM) eviction.
- **Negative (Developer Experience):** Agents cannot download executable binaries at runtime or write state to local disk; all state must be handled in memory or written to authorized external storage.
