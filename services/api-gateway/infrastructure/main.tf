resource "google_container_cluster" "primary" {
  count    = var.enable_infra ? 1 : 0
  name     = "dev-gke-cluster"
  location = "us-central1"
  initial_node_count = 1
  remove_default_node_pool = true
}

resource "google_container_node_pool" "primary_nodes" {
  count      = var.enable_infra ? 1 : 0
  name       = "dev-node-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.primary[0].name
  node_count = 5
}

resource "google_sql_database_instance" "litellm_db" {
  name             = "litellm-db"
  database_version = "POSTGRES_15"
  region           = "us-central1"
  settings {
    tier              = "db-custom-1-3840"
    activation_policy = var.enable_infra ? "ALWAYS" : "NEVER"
  }
  deletion_protection = false

  lifecycle {
    ignore_changes = [
      settings[0].tier,
      settings[0].database_flags,
      settings[0].enable_dataplex_integration,
      deletion_protection
    ]
  }
}
