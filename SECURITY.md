# Security Policy

## Incident Reporting
If you discover a potential security vulnerability in the SAGC, please report it via [brian.lasky@email.com]. 

## Security Posture
The SAGC adheres to the following principles:
- **Least Privilege:** The service runs with minimal container capabilities.
- **Fail-Closed:** Governance failures default to a denied state.
- **Auditability:** All budget modifications are tracked via Git commit history, ensuring an immutable audit trail for fiscal governance.