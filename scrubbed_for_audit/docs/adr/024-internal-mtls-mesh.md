# ADR 024: Internal Mutual TLS (mTLS) Mesh Infrastructure

## Status
Accepted

## Context
While external ingress and egress boundaries are hardened, internal service-to-service communication between autonomous agents and the SAGC Gateway occurs over cleartext HTTP. If a single workload inside the cluster is compromised, an attacker could intercept raw prompts, context windows, and API responses.

## Decision
We enforce strict cryptographic identity and mutual TLS (mTLS) for all internal pod-to-pod communication.
1. We will leverage a Kubernetes Service Mesh (such as Istio or Google Anthos Service Mesh) to manage service identities via short-lived SPIFFE x509 certificates.
2. We will deploy a mesh-wide `PeerAuthentication` policy configured in `STRICT` mode for the namespaces running our agentic workloads and the SAGC gateway.
3. Any unencrypted cleartext connection or connection with an unverified SPIFFE identity will be dropped immediately at the pod network boundary by the Envoy proxy sidecar.

## Consequences
* **Positive:** Complete cryptographic protection for internal prompt transit; satisfies strict data-in-transit regulatory mandates without altering agent application code.
* **Negative:** Introduces minimal sidecar proxy CPU/memory overhead for mutual cryptographic handshakes; requires careful tracking of non-mesh cluster components (like core Kubernetes DNS or monitoring metrics scrapers) to prevent communication breakage.
