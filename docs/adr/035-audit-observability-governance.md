# ADR 035: Audit Observability & Rate Limiting

## Status
Proposed

## Context
To prevent log pollution and ensure ADR 014 (Immutable Audit Logs) integrity, we require structured log emission and per-agent rate limiting. Relying on generic `print()` statements is insufficient for high-velocity agentic workloads.

## Decision
1. All fiscal governance events shall be emitted via a structured `emit_audit_event` helper, outputting JSON to `stdout`.
2. A local, in-memory rate limiter shall be enforced at the application layer to cap audit event volume (100 events/minute/agent) to prevent log-sink exhaustion.
3. Audit logs must conform to the schema required by the `sagc-audit-sink` filter defined in `logging.tf`.

## Consequences
* **Positive:** Guaranteed log-sink availability during attacks; provides canonical audit records.
* **Negative:** In-memory rate limiting is not shared across distributed pods (an agent might exceed the 100-event limit by hitting multiple pods), requiring a future migration to a Redis-backed rate limiter if strictly required.
