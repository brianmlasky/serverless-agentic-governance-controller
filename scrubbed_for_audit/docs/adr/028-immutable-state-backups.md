# ADR 028: Immutable State Backups (Point-In-Time Recovery)

## Status
Accepted

## Context
The SAGC architecture relies on a distributed Redis state store for real-time token budgeting and velocity rate limiting. If this state is corrupted, deleted, or encrypted via ransomware, the governance controller loses its fiscal tracking capability, resulting in either unbounded spend or a complete fleet outage.

## Decision
We implement Point-In-Time Recovery (PITR) utilizing immutable external storage.
1. Redis will be configured to generate continuous Append-Only File (AOF) streams and hourly RDB snapshots.
2. A sidecar backup agent (e.g., Wal-G or a custom cron container) will continuously ship these artifacts to a dedicated Google Cloud Storage bucket.
3. This backup bucket will reside in a heavily isolated, dedicated "Backup/Archive" GCP project.
4. The bucket will have Object Lock (WORM) enabled with a 30-day retention policy, ensuring that even a compromised `roles/owner` in the primary production project cannot delete or alter the backups.

## Consequences
* **Positive:** Guarantees a near-zero Recovery Point Objective (RPO) and protects against catastrophic administrative error or ransomware targeting the state store.
* **Negative:** Increases storage costs and introduces minor disk I/O overhead on the Redis primary node to process and ship the continuous AOF streams.
