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
    auto {}
  }
}

# Cryptographic/Technical Guardrail: Least-Privilege IAM Access Path
# Grants ONLY the runtime identity the capability to pull secret payloads
resource "google_secret_manager_secret_iam_member" "litellm_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.llm_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"

  # This implicit reference resolves the race condition by forcing Terraform to 
  # wait until the service account API fully propagates the identity.
  member = "serviceAccount:${google_service_account.litellm_wif.email}"

  depends_on = [
    google_secret_manager_secret.llm_api_key
  ]
}

# 1. Generate a high-entropy 32-character cryptographic secret
resource "random_password" "fencing_secret_value" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# 2. Define the Google Secret Manager resource
resource "google_secret_manager_secret" "sagc_fencing_secret" {
  secret_id = "sagc-fencing-secret"
  
  replication {
    auto {}
  }

  labels = {
    environment = var.environment
    component   = "sagc-governance"
    finops-tier = "critical"
  }
}

# 3. Store the generated password inside the GCP Secret
resource "google_secret_manager_secret_version" "sagc_fencing_secret_version" {
  secret      = google_secret_manager_secret.sagc_fencing_secret.id
  secret_data = random_password.fencing_secret_value.result
}