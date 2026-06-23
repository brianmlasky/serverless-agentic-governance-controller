# ADR 017: Spend Velocity Rate Limiting (Token Bucket)

## Decision
We utilize a Redis-backed Token Bucket algorithm (via atomic Lua scripting) to enforce a requests-per-minute velocity limit on all autonomous agents, preventing instantaneous budget depletion during infinite loops.
