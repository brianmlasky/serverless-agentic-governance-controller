# tests/chaos_test_runaway.py
import sys
import os
import requests
import concurrent.futures

# Point to the local Envoy Proxy / API Gateway egress endpoint
PROXY_URL = os.getenv("SAGC_PROXY_URL", "http://localhost:8080/v1/chat/completions")
AGENT_ID = os.getenv("TEST_AGENT_ID", "chaos-agent-999")

def fire_request():
    """Simulates a single outbound LLM call from an AI agent."""
    headers = {
        "Content-Type": "application/json",
        "x-internal-agent-id": AGENT_ID
    }
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Simulate runaway recursive loop"}]
    }
    try:
        # Rapid timeout to simulate high-velocity network flooding
        response = requests.post(PROXY_URL, headers=headers, json=payload, timeout=2)
        return response.status_code
    except requests.exceptions.RequestException:
        return 503 # Service Unavailable / Proxy down

def simulate_runaway(concurrency=50, total_requests=200):
    print(f"--- 🌪️ Chaos Injection: Starting Runaway Simulation ---")
    print(f"[METRIC] Flooding egress proxy with {concurrency} concurrent threads...")
    
    status_counts = {}
    
    # Slam the proxy with concurrent requests to test atomic race conditions
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(fire_request) for _ in range(total_requests)]
        for future in concurrent.futures.as_completed(futures):
            status = future.result()
            status_counts[status] = status_counts.get(status, 0) + 1

    print("\n[RESULTS] Egress HTTP Status Distribution:")
    for status, count in status_counts.items():
        print(f"  HTTP {status}: {count} requests")

    # The Principal Assertion: We MUST see HTTP 429s indicating the budget snapped shut.
    if 429 in status_counts:
        print("\n[SUCCESS] OPA Sidecar successfully trapped the runaway agent.")
        print("[CRITICAL] HTTP 429 (Too Many Requests) intercepted. Fiscal circuit breaker active.")
        sys.exit(0) # Pipeline passes
    elif 200 in status_counts and len(status_counts) == 1:
        print("\n[FATAL] OPA Policy bypassed! Budget exhausted but proxy allowed all traffic.")
        sys.exit(1) # Pipeline fails
    else:
        print("\n[WARNING] Indeterminate state. Check proxy configuration.")
        sys.exit(1)

if __name__ == "__main__":
    simulate_runaway()