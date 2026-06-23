import json
import logging
import sys
from datetime import datetime

def emit_audit_event(event_type: str, status: str, agent_id: str, details: dict):
    """
    Standardized log emitter for the SAGC Audit Sink.
    Ensures all logs match the jsonPayload filter requirements.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "fiscal_event" if event_type == "fiscal" else "governance_event",
        "status": status,
        "agent_id": agent_id,
        "details": details,
        "version": "1.0"
    }
    # Direct output to stdout for the K8s logging agent (Fluentd/FluentBit)
    sys.stdout.write(json.dumps(log_entry) + "\n")
    sys.stdout.flush()

# Usage Example:
# emit_audit_event("fiscal", "deny", "agent-007", {"reason": "INSUFFICIENT_FUNDS", "token": 45})