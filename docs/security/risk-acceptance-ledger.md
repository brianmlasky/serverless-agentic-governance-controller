# Security Risk Acceptance Ledger

## CVE-2026-0994 (Protobuf DoS)
* **Date Accepted:** June 11, 2026
* **Component:** `sagc-controller`
* **Justification:** Upstream GCP libraries (`google-api-core`, `grpcio`) strictly pin `protobuf < 5.0.0`, preventing an upgrade to the patched version (5.29.6). 
* **Exploitability Analysis:** This CVE requires parsing deeply recursive, untrusted protobuf payloads. The SAGC only parses internal, authenticated JSON AdmissionReview requests from the Kubernetes Control Plane. The attack vector is inaccessible.
* **Status:** Risk Accepted. Suppressed via `.trivyignore` until Google releases updated client libraries.

## CVE-2026-23949 (jaraco.context Path Traversal) & CVE-2026-24049 (wheel Privilege Escalation)
* **Date Accepted:** June 11, 2026
* **Component:** `sagc-controller` (Build Tooling)
* **Justification:** These vulnerabilities exist within the vendored dependencies of `setuptools` (`setuptools/_vendor/jaraco.context` and `setuptools/_vendor/wheel`). They cannot be patched via standard `pip` pinning.
* **Exploitability Analysis:** Both CVEs require the extraction of maliciously crafted `.tar` or `.whl` archives. The SAGC container does not dynamically fetch or extract untrusted packages at runtime. These tools are only invoked during the immutable CI build phase against verified dependencies. The runtime risk is zero.
* **Status:** Risk Accepted. Suppressed via `.trivyignore` until the base Python image updates its `setuptools` distribution.
