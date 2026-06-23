# Google Artifact Registry for Immutable Container Provenance
resource "google_artifact_registry_repository" "agentic_proxy_repo" {
  location      = "us-central1"
  repository_id = "agentic-proxy-repo"
  description   = "Docker repository for Serverless Agentic Governance Controller workloads (LiteLLM, Agents)"
  format        = "DOCKER"

  # Enforce immutable tags to prevent supply chain tampering and rollback attacks
  docker_config {
    immutable_tags = true
  }
}