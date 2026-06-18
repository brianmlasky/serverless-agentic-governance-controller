# ADR 027: Automated Upstream API Key Rotation

## Status
Accepted

## Context
The SAGC Gateway authenticates with external LLM providers (e.g., OpenAI, Anthropic) using static API keys stored in GCP Secret Manager. Long-lived static credentials represent a severe supply chain and fiscal risk if exposed.

## Decision
We enforce cryptographic agility for all external LLM provider credentials via an automated rotation pipeline.
1. A secure, scheduled runner (e.g., a Cloud Run job triggered via Cloud Scheduler) will execute a key rotation script every 30 days.
2. The runner will authenticate to the upstream LLM provider's management API, generate a new API key, and write the new key to GCP Secret Manager as a new version.
3. The runner will then trigger a rolling restart of the SAGC Gateway Kubernetes deployment to ensure all Envoy/LiteLLM pods load the fresh credential.
4. The runner will explicitly revoke the old API key via the provider's API after a 24-hour grace period to ensure no inflight requests are dropped.

## Consequences
* **Positive:** Drastically limits the exposure window of a compromised downstream credential; eliminates manual toil associated with secret rotation.
* **Negative:** Introduces complex orchestration logic; provider API outages during the rotation window could temporarily block the issuance of new keys.
