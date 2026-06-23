# Architectural Decision Records (ADRs)

## Decision 001: File-based State Storage vs. Redis
- **Context:** We needed a way to track budget usage that is atomic and simple to audit.
- **Decision:** Implemented a local JSON file store with atomic `f.seek()`/`f.truncate()` operations.
- **Trade-offs:** - *Pro:* Zero-infrastructure dependency, perfect for testing/CI, easy to audit via Git.
    - *Con:* Not suitable for multi-node K8s deployments (requires shared volume or migration to Redis).
- **Result:** Successfully achieved "Policy-as-Code" goal with minimal complexity.