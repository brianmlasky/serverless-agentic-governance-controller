# terraform/logging.tf

resource "google_storage_bucket" "audit_logs" {
  name          = "sagc-audit-logs-immutable"
  location      = "US"
  force_destroy = false # Safety first

  retention_policy {
    is_locked        = true # Set to true ONLY after validation
    retention_period = 31536000 # 365 days
  }
}

resource "google_logging_project_sink" "sagc_audit_sink" {
  name        = "sagc-audit-sink"
  destination = "storage.googleapis.com/${google_storage_bucket.audit_logs.name}"
  filter      = "protoPayload.methodName:* AND protoPayload.serviceName:*"
}