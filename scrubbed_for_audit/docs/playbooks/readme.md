# Incident Playbooks & Runbooks

This directory contains the operational playbooks for incident response and recovery.

## Runbook Structure Standard (Elite-Grade)

All entries in the failure scenarios playbook must adhere to the following structure. Unlike "junior" runbooks that suggest guessing or checking arbitrary logs, an "elite" runbook relies on explicit queries, automated alerts, and safe bypass mechanisms.

1.  **Symptom:** What does the team see in the dashboards? (Explicit metrics).
2.  **Immediate Impact:** What is breaking for the user or the business?
3.  **The "Stop Work" Trigger:** When do we pause and call a formal P0/P1 incident?
4.  **Forensic Strategy:** What telemetry do we check first? (The precise "Triangulation" plan and queries).
5.  **Recovery Plan:** The most stable path to restoration (e.g., specific rollback commands, circuit breaker toggles, or configuration adjustments).
