# ADR 016: Zero-Trust Ingress via Cloud IAP

## Status
Accepted

## Context
Exposing the SAGC API Gateway directly to the public internet invites DDoS attacks and unauthenticated probing, wasting GKE compute resources.

## Decision
We implement a Zero-Trust ingress architecture using Google Cloud Identity-Aware Proxy (IAP) via a GKE `BackendConfig`. Traffic is authenticated cryptographically at the Google Edge before routing to the VPC.
