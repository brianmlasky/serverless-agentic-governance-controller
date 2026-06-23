variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy the Redis instance"
  type        = string
  default     = "us-central1"
}

variable "network_id" {
  description = "The VPC network ID to peer the Redis instance with"
  type        = string
}

# 1. Provision a Highly Available Memorystore Cluster
resource "google_redis_instance" "sagc_cache" {
  name           = "sagc-ha-redis"
  project        = var.project_id
  region         = var.region
  
  tier           = "STANDARD_HA"
  memory_size_gb = 1

  authorized_network = var.network_id
  connect_mode       = "PRIVATE_SERVICE_ACCESS"

  redis_version = "REDIS_6_X"
  display_name  = "SAGC High-Availability Governance Cache"

  labels = {
    environment = "test"
    component   = "sagc-governance"
    finops-tier = "ephemeral"
  }
}

output "redis_host" {
  value       = google_redis_instance.sagc_cache.host
}