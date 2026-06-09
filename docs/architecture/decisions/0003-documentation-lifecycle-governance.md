# ADR 0003: Documentation Lifecycle Governance and Anti-Drift Policies

## Status
Accepted

## Context
Documentation drift is a critical failure of platform governance. Manual documentation degrades velocity, creates trust deficits, and impedes onboarding.

## Decision Outcome
We are instituting a "Docs as Code" strict lifecycle policy utilizing two core techniques:
1. **Automated Extraction:** Infrastructure operational readmes must be generated dynamically from code outputs.
2. **Frontmatter TTLs:** All manually maintained operational documentation must include a YAML Time-To-Live (TTL) header. Documents exceeding their expiration date will be flagged for mandatory freshness review by their defined owner.

This ensures the platform's memory remains synchronized with its executing state.
