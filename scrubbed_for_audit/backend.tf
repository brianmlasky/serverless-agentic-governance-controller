terraform {
  required_version = ">= 1.8.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30.0"
    }
  }

  backend "gcs" {
    bucket = "tf-state-alert-hall-466720-c0"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = "alert-hall-466720-c0"
  region  = "us-central1"
}