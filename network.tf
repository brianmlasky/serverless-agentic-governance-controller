# The primary Virtual Private Cloud (VPC)
resource "google_compute_network" "vpc_network" {
  name                    = "sagc-vpc"
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

# The dedicated Subnet for the GKE Cluster
resource "google_compute_subnetwork" "gke_subnet" {
  name          = "sagc-gke-subnet"
  ip_cidr_range = "10.0.0.0/16"
  region        = "us-central1"
  network       = google_compute_network.vpc_network.id

  # Alias IP ranges required for VPC-native GKE clusters
  secondary_ip_range {
    range_name    = "gke-pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "gke-services"
    ip_cidr_range = "10.2.0.0/20"
  }
}
# Trigger CI/CD execution
# Retry CI/CD initialization
