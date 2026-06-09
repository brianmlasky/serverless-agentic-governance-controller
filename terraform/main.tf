# ------------------------------------------------------------------
# Root Infrastructure Deployment
# ------------------------------------------------------------------

# 1. Create Core Service Accounts
resource "google_service_account" "sagc_controller" {
  project      = var.project_id  # Explicit project binding
  account_id   = "sagc-controller"
  display_name = "SAGC Controller Service Account"
}

resource "google_service_account" "litellm_wif" {
  project      = var.project_id  # Explicit project binding
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