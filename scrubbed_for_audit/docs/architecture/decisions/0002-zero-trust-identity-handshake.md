# ADR 0002: Zero-Trust Keyless Identity Handshake for CI/CD and Runtime Workloads

## Status
Accepted

## Context and Problem Statement
Our Serverless Agentic Governance Controller (SAGC) requires programmatic access to Google Cloud Platform (GCP) at two distinct boundaries:
1. CI/CD Delivery Boundary: The GitHub Actions automation runner needs permissions to push compiled controller images.
2. Runtime Workload Boundary: Pods executing inside our GKE cluster need permissions to pull cryptographic tokens.

Historically, this was achieved by exporting long-lived, static IAM Service Account JSON keys. This pattern introduces severe vulnerabilities, lacks attribution, and violates governance compliance.

## Decision Outcome
Chosen Option: Workload Identity Federation (OIDC Token Exchange).

By establishing an OIDC trust boundary, GCP directly validates short-lived OpenID Connect tokens minted dynamically by GitHub Actions and GKE. 
* Positive: Zero private keys stored, granular repository/namespace conditions, self-expiring tokens.
* Negative: Initial setup friction regarding OIDC claim mapping.

## Infrastructure Mapping State
* Identity Pool: sagc-pool
* Target Execution Identity: sagc-controller@alert-hall-466720-c0.iam.gserviceaccount.com
