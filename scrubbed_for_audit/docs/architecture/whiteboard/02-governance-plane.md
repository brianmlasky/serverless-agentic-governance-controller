# Whiteboard View 2: The State & Governance Plane

**Purpose:** To demonstrate how the SAGC ensures policy integrity, identity, and financial observability across a distributed AI environment without creating a single point of failure.

## The Architectural Pillars
1. **GitOps Reconciliation:** All policies are defined as Rego files in Git; Flux/ArgoCD ensures production parity.
2. **Identity Plane (SPIFFE/SPIRE):** Every sidecar has a short-lived x509 SVID to authenticate against the policy store.
3. **FinOps Telemetry Loop:** Redis-based budget aggregation with an automatic "hard-cap" push-back mechanism.

## The Talk Track
* **Policy Source of Truth:** "We treat governance as code. Policies are version-controlled Rego files. When a PR is merged, our GitOps controller pulls the state, guaranteeing that what's in Git is exactly what's running in the cluster."
* **Identity Plane:** "We don't trust pods by IP. Every OPA sidecar uses SPIFFE/SPIRE to present a short-lived, cryptographically signed identity to the policy store, ensuring no rouge pod can pull internal governance rules."
* **FinOps Telemetry Loop:** "We aggregate budget metrics into Redis. If a namespace hits 95% of its hard-cap, our aggregator sends an API signal back to that specific OPA sidecar to update its local 'block-all' variable in real-time."

## Proactive Defense (The "Means Test")
**The Risk:** Stale Policy Propagation.
**The Fix:** 'Enforce-or-Die' heartbeat. If the sidecar fails to receive a policy sync for longer than the TTL threshold, it defaults to a 'Block-All' state—because we prioritize compliance and security over availability during a governance control plane failure.