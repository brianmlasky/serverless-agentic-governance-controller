import sys
import time

def simulate_runaway(threshold):
    print(f"--- Chaos Injection: Starting Runaway Simulation (Threshold: {threshold}%) ---")
    print("[METRIC] Simulating agentic token burn...")
    
    # In a live cluster, this queries the OPA sidecar. 
    # For CI verification, we simulate the OPA response engine.
    if threshold >= 100:
        print("[CRITICAL] OPA Policy dictates Hard Kill. Executing Fail-Closed termination.")
        sys.exit(1)
    elif threshold >= 90:
        print("[THROTTLE] OPA Policy dictates Rate Limiting.")
    elif threshold >= 80:
        print("[ALERT] OPA Policy dictates FinOps Warning.")
    else:
        print("[OK] OPA Policy allows continued execution.")

if __name__ == "__main__":
    simulate_runaway(100)
