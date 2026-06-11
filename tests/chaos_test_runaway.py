import requests
import sys

OPA_URL = "http://localhost:8181/v1/data/sagc/fiscal"

def evaluate_fiscal_state(current_consumption):
    # 1. Ask OPA for the policy decision
    payload = {"input": {"consumption_percentage": current_consumption}}
    response = requests.post(OPA_URL, json=payload).json()
    
    decisions = response.get("result", {})
    
    # 2. Enforce the decision blindly
    if decisions.get("hard_kill"):
        print("[CRITICAL] OPA Policy dictates Hard Kill. Terminating workload.")
        sys.exit(1)
    elif decisions.get("throttle"):
        print("[THROTTLE] OPA Policy dictates Rate Limiting.")
    elif decisions.get("alert"):
        print("[ALERT] OPA Policy dictates FinOps Warning.")
    else:
        print("[OK] OPA Policy allows continued execution.")