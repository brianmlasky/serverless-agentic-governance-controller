# Security Risk Acceptance Ledger

## CVE-2026-0994 (Protobuf DoS)
* **Date Accepted:** June 11, 2026
* **Component:** `sagc-controller`
* **Justification:** Upstream GCP libraries (`google-api-core`, `grpcio`) strictly pin `protobuf < 5.0.0`, preventing an upgrade to the patched version (5.29.6). 
* **Exploitability Analysis:** This CVE requires parsing deeply recursive, untrusted protobuf payloads. The SAGC only parses internal, authenticated JSON AdmissionReview requests from the Kubernetes Control Plane. The attack vector is inaccessible.
* **Status:** Risk Accepted. Suppressed via `.trivyignore` until Google releases updated client libraries.
