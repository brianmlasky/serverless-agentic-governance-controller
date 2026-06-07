# ==========================================================================
# Google Secret Manager: Vault Allocation for Agentic Governance Proxy
# ==========================================================================

# Define the logical slot for the LLM API Key
resource "google_secret_manager_secret" "llm_api_key" {
  secret_id = "litellm-provider-api-key"

  labels = {
    environment = "production"
    managed-by  = "terraform"
    application = "serverless-agentic-governance-controller"
  }

  # Enforce automatic replication across Google managed regions
  replication {
    automatic = true
  }
}

# Cryptographic/Technical Guardrail: Least-Privilege IAM Access Path
# Grants ONLY the runtime identity the capability to pull secret payloads
resource "google_secret_manager_secret_iam_member" "litellm_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.llm_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:litellm-wif-sa@alert-hall-466720-c0.iam.gserviceaccount.com"

  depends_on = [
    google_secret_manager_secret.llm_api_key
  ]
}