terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "alert-hall-466720-c0-terraform-state"
    prefix = "environments/dev-aws"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = "serverless-agentic-platform"
      ManagedBy   = "terraform"
    }
  }
}

module "aws_iam" {
  source = "../../modules/aws-iam"

  aws_account_id      = var.aws_account_id
  admin_user_name     = var.admin_user_name
  gcp_project_id      = var.gcp_project_id
  gcp_region          = var.gcp_region
  gke_cluster_name    = var.gke_cluster_name
  k8s_namespace       = var.k8s_namespace
  k8s_service_account = var.k8s_service_account
  environment         = var.environment

  gke_oidc_provider_arn = "arn:aws:iam::${var.aws_account_id}:oidc-provider/container.googleapis.com/v1/projects/${var.gcp_project_id}/locations/${var.gcp_region}/clusters/${var.gke_cluster_name}"
  gke_oidc_provider_url = "container.googleapis.com/v1/projects/${var.gcp_project_id}/locations/${var.gcp_region}/clusters/${var.gke_cluster_name}"
}

# ---------------------------------------------------------------------------
# Account ID guard - fails plan if injected var != actual caller identity
# ---------------------------------------------------------------------------
data "aws_caller_identity" "current" {}

locals {
  account_id_verified = (
    var.aws_account_id == data.aws_caller_identity.current.account_id
    ? var.aws_account_id
    : tobool("ERROR: aws_account_id var (${var.aws_account_id}) does not match caller identity (${data.aws_caller_identity.current.account_id})")
  )
}
