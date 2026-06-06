# This bucket intentionally violates security standards to test tfsec
resource "google_storage_bucket" "insecure_test_bucket" {
  name          = "sagc-insecure-test-bucket-123"
  location      = "US"
  force_destroy = true
  
  # MISSING: uniform_bucket_level_access = true
  # MISSING: public_access_prevention = "enforced"
}
