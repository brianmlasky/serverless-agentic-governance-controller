# ------------------------------------------------------------------
# IAM Federation for GKE and GitHub Actions
# ------------------------------------------------------------------

variable "project_id" { type = string }
variable "k8s_service_account" { type = string }
variable "github_repo" { type = string }
variable "aws_role_arn" { type = string }

resource "google_iam_workload_identity_pool" "sagc_pool" {
  workload_identity_pool_id = "sagc-pool"
  project                   = var.project_id
}

resource "google_iam_workload_identity_pool_provider" "gke_provider" {
  project                            = var.project_id # Explicit project binding added
  workload_identity_pool_id          = google_iam_workload_identity_pool.sagc_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "gke-provider"

  attribute_mapping = {
    "google.subject" = "assertion.sub"
  }

  oidc {
    issuer_uri = "https://container.googleapis.com/v1/projects/${var.project_id}/locations/global/clusters/dev-sagc-cluster"
  }
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  project                            = var.project_id # Explicit project binding added
  workload_identity_pool_id          = google_iam_workload_identity_pool.sagc_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-actions"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }

  attribute_condition = "assertion.repository == \"${var.github_repo}\""

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account_iam_member" "gke_workload_identity_binding" {
  service_account_id = "projects/${var.project_id}/serviceAccounts/sagc-controller@${var.project_id}.iam.gserviceaccount.com"
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[agentic/${var.k8s_service_account}]"
}

resource "google_service_account_iam_member" "github_workload_identity_binding" {
  service_account_id = "projects/${var.project_id}/serviceAccounts/sagc-controller@${var.project_id}.iam.gserviceaccount.com"
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.sagc_pool.name}/attribute.repository/${var.github_repo}"
}