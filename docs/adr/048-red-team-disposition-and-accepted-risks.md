# ADR-048: Disposition of Adversarial Red Team Findings

## Status
Accepted

## Context
A Staff-level adversarial architecture audit yielded several critical findings. While the core vulnerabilities (Double-Spend, Fail-Open proxies, and SPIFFE spoofing) were remediated via ADRs 045, 046, and 047, several structural recommendations were made regarding observability and causal ordering.

## Decision
1. **Reject Kafka/PubSub for Lamport Clocks:** The recommendation to introduce Kafka for causal event ordering is rejected to maintain the "Serverless" operational profile of the SAGC. WORM-compliant GCS buckets are deemed sufficient for eventual-consistency forensics.
2. **Accept eBPF/Falco Exhaustion Risk:** Falco is acknowledged as a lossy IDS under extreme syscall load. The primary enforcement boundary remains the fail-closed Envoy proxy mesh.
3. **Accept Localized DoS (Livelock/Timeout):** The system prioritizes security over availability. OPA livelocks or Presidio container exhaustion will result in Envoy timeouts, severing network access. This localized DoS is an accepted operational tradeoff to guarantee zero uninspected LLM egress.

## Consequences
Maintains a lean, low-overhead control plane while strictly enforcing the Zero-Trust fiscal and data boundaries.
