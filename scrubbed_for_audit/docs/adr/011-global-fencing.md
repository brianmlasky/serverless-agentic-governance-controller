# ADR 011: Global Fencing for Active-Passive Failover

## Decision
We implement a distributed Redis lease (Redlock) as the "Source of Truth" for region-wide authorization. 

## Rationale
Prevents budget collision during multi-cloud failover events where split-brain state could lead to OpEx double-spend.

## Fencing Policy
All `sagc` ingress/egress is gated by the `is_primary_environment` policy check.
