terraform {
  backend "gcs" {
    bucket  = "tf-state-alert-hall-466720-c0"
    prefix  = "terraform/state"
  }
}
