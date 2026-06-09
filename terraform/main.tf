# ------------------------------------------------------------------
# Root Infrastructure Deployment
# ------------------------------------------------------------------

# 1. Create Core Service Accounts
resource "google_service_account" "sagc_controller" {
  project      = var.project_id # Explicit project binding
  account_id   = "sagc-controller"
  display_name = "SAGC Controller Service Account"
}

resource "google_service_account" "litellm_wif" {
  project      = var.project_id # Explicit project binding
  account_id   = "litellm-wif-sa"
  display_name = "LiteLLM WIF Service Account"
}

# 2. Identity Federation Module
module "workload_identity" {
  source = "./modules/iam-federation"

  project_id          = var.project_id
  k8s_service_account = "sagc-agent-sa"
  github_repo         = "brianmlasky/serverless-agentic-governance-controller"
  aws_role_arn        = "arn:aws:iam::123456789012:role/sagc-dr-failover"

  depends_on = [google_service_account.sagc_controller]
}

# 3. Artifact Registry Module
module "artifact_registry" {
  source      = "./modules/artifact-registry"
  project_id  = var.project_id
  region      = "us-central1"
  environment = "production"
}

# 4. Supply Chain Authorization
# Grant the pipeline identity explicit permission to push to the governed registry
resource "google_artifact_registry_repository_iam_member" "repo_writer" {
  project    = var.project_id
  location   = "us-central1"
  repository = module.artifact_registry.repository_id
  role       = "roles/artifactregistry.writer"

  # Cryptographic binding directly to the runtime identity
  member = "serviceAccount:${google_service_account.sagc_controller.email}"
}