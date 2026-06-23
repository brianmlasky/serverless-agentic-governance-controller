# ------------------------------------------------------------------
# Operational Outputs for Identity Governance
# ------------------------------------------------------------------

output "wif_provider_uri" {
  description = "The fully qualified Workload Identity Provider URI for GitHub Actions"
  value       = "projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/sagc-pool/providers/github-actions"
}

output "controller_service_account_email" {
  description = "The runtime service account for the governance controller"
  value       = google_service_account.sagc_controller.email
}
