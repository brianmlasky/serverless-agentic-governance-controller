# Incident Management Standard: The Commander Protocol

During a P0/P1 incident, the Principal Architect assumes the role of **Incident Commander** (Orchestrator) and strictly abstains from typing or executing commands (Operator).

## Phase 1: Stabilize
*   Prioritize recovery (e.g., immediate rollback to the last stable SHA) over root-cause analysis.

## Phase 2: Role Assignment
*   **The Scribe:** Documents all actions in real-time for the post-mortem audit trail.
*   **The Operator:** The single individual authorized to execute commands.
*   **The Scout:** Analyzes logs, metrics, and telemetry for patterns.
*   **The Comms Lead:** Isolates the engineering team by handling all stakeholder updates.

## Phase 3: Communication & Safety
*   **Closed-Loop Communication:** Enforce explicit confirmation of actions (e.g., "I am restarting Service A" -> "Understood, restarting Service A").
*   **Stop Work Authority:** Any engineer possesses the absolute authority to halt a remediation process if they believe it compromises Data Integrity. Safety > Uptime.
