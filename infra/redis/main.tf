provider "google" {
  project = "alert-hall-466720-c0"
  region  = "us-central1"
}

resource "google_redis_instance" "sagc_budget_store" {
  name               = "sagc-budget-store"
  tier               = "BASIC"
  memory_size_gb     = 1
  region             = "us-central1"
  # Updated to target the correct GKE VPC
  authorized_network = "projects/alert-hall-466720-c0/global/networks/dev-vpc"
  redis_version      = "REDIS_7_0"
}

output "redis_ip" {
  value = google_redis_instance.sagc_budget_store.host
}
