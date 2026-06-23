terraform {
  required_version = ">= 1.7.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  backend "gcs" {
    bucket = "alert-hall-466720-c0-terraform-state"
    prefix = "environments/dev"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

provider "aws" {
  region = var.aws_region
}

data "google_project" "current" {
  project_id = var.project_id
}

locals {
  gke_node_sa = "${data.google_project.current.number}-compute@developer.gserviceaccount.com"
}

# ── Networking ─────────────────────────────────────────────────────────────
module "networking" {
  source      = "../../modules/networking"
  project_id  = var.project_id
  region      = var.region
  environment = var.environment
}

# ── Private Service Access (Required for Memorystore) ──────────────────────
# Define the IP range used for Private Service Access
resource "google_compute_global_address" "private_ip_range" {
  name          = "google-managed-services-dev-vpc"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = module.networking.network_id
}

# Bind the service connection to that range
resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = module.networking.network_id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_range.name]
}

# ── Artifact Registry ──────────────────────────────────────────────────────
module "artifact_registry" {
  source      = "../../modules/artifact-registry"
  project_id  = var.project_id
  region      = var.region
  environment = var.environment

  reader_service_accounts = [local.gke_node_sa]
}

# ── GKE Autopilot ─────────────────────────────────────────────────────────
module "gke_autopilot" {
  source              = "../../modules/gke-autopilot"
  project_id          = var.project_id
  region              = var.region
  environment         = var.environment
  cluster_name        = "sagc-cluster"
  network_name        = module.networking.network_name
  subnetwork_name     = module.networking.subnetwork_name
  pods_range_name     = module.networking.pods_range_name
  services_range_name = module.networking.services_range_name

  depends_on = [module.networking]
}

# ── AWS IAM (Bedrock access via GKE Workload Identity) ────────────────────
module "aws_iam" {
  source = "../../modules/aws-iam"

  environment          = var.environment
  aws_account_id       = var.aws_account_id
  gke_cluster_project  = var.project_id
  gke_cluster_location = var.region
  gke_cluster_name     = var.gke_cluster_name
  k8s_namespace        = "agentic"
  k8s_service_account  = "litellm-wif-sa"
}

# ── GitHub Actions CI/CD Service Account (Commented out to resolve state drift) ──
/*
resource "google_service_account" "github_actions_sa" {
  project      = var.project_id
  account_id   = "github-actions-sa"
  display_name = "GitHub Actions CI/CD Service Account"
}

resource "google_iam_workload_identity_pool" "github_pool" {
  project                   = var.project_id
  workload_identity_pool_id = "github-actions-pool"
  display_name              = "GitHub Actions Pool"
}
*/

# ── LiteLLM Workload Identity ─────────────────────────────────────────────
module "workload_identity" {
  source = "../../modules/workload-identity"

  project_id             = var.project_id
  aws_role_arn           = module.aws_iam.role_arn
  k8s_namespace          = "agentic"
  k8s_service_account    = "litellm-wif-sa"
  environment            = var.environment
  gke_cluster_dependency = module.gke_autopilot.cluster_name
  project_roles          = ["roles/cloudsql.client"]
  
  sagc_fencing_secret_id = google_secret_manager_secret.sagc_fencing_secret.id

  depends_on = [module.gke_autopilot, module.aws_iam]
}

# ── High-Availability Memorystore (Redis) ─────────────────────────────────
module "redis" {
  source     = "../../modules/redis"
  project_id = var.project_id
  region     = var.region
  network_id = module.networking.network_id 
}