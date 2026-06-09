# ------------------------------------------------------------------
# Artifact Registry: Governed Image Supply Chain
# ------------------------------------------------------------------

resource "google_artifact_registry_repository" "controller_repo" {
  project       = var.project_id
  location      = var.region
  repository_id = "sagc-images"
  description   = "Docker repository for the Serverless Agentic Governance Controller"
  format        = "DOCKER"

  cleanup_policies {
    id     = "keep-recent-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count = 5
    }
  }
}

output "repository_name" {
  value = google_artifact_registry_repository.controller_repo.name
}
