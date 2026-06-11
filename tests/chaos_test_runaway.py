import time
import sys

def simulate_runaway(threshold):
    print(f"--- Chaos Injection: Starting Runaway Simulation (Threshold: {threshold}%) ---")
    print("[METRIC] Simulating agentic token burn...")
    
    if threshold >= 80:
        print("[ALERT] 80% Threshold Reached. Dispatching asynchronous webhook warning.")
    if threshold >= 90:
        print("[THROTTLE] 90% Threshold Reached. Injecting artificial latency into LLM requests.")
        time.sleep(1)
    if threshold >= 100:
        print("[CRITICAL] 100% Budget Exhausted. Executing Fail-Closed Hard Kill.")
        sys.exit(1)
        
if __name__ == "__main__":
    # In a real CI environment, this parameter would be dynamic
    simulate_runaway(100)