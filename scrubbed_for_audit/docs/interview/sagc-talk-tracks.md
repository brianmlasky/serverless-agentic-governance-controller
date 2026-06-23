# SAGC Interview Talk Tracks

## Scenario: Implementing Guardrails without impacting Velocity
1. **Shift-Left Validation:** Treat governance as a CI/CD pre-flight check rather than a production-time blocker.
2. **Deterministic Performance:** Decouple policy evaluation from the critical path using thread-safe, local caching.
3. **Graceful Degradation:** Implement "fail-closed" logic for fiscal hard limits while allowing "fail-open" for non-critical telemetry to maintain uptime.