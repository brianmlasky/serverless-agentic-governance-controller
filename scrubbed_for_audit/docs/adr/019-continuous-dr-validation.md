# ADR 019: Continuous Disaster Recovery Validation (Chaos Engineering)

## Status
Accepted

## Context
Our active-passive multi-cloud architecture relies on a Redis-backed Global Fencing Lock (ADR 011) to prevent split-brain budget consumption. Failover mechanisms are notoriously prone to configuration drift and silent decay over time.

## Decision
We will implement an automated Chaos Engineering practice for our DR mechanisms:
1. A Kubernetes `CronJob` (the "Chaos Monkey") will be deployed in our staging environments.
2. On a scheduled cadence, it will intentionally delete the `global-primary-lock` or introduce network latency to the Redis state store.
3. Our telemetry must confirm that the SAGC Envoy proxies instantly enter a "Fail-Closed" state, dropping all outbound LLM traffic until the lease is recovered or promoted to the passive region.

## Consequences
* **Positive:** Transforms DR from a theoretical binder of runbooks into a cryptographically verified, continuous metric.
* **Negative:** Introduces intentional instability into staging environments; requires sophisticated synthetic monitoring to measure the success of the chaos experiments.
