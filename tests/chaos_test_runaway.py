import os
import requests
import time

PROXY_URL = os.getenv("SAGC_PROXY_URL", "http://localhost:4000/v1/chat/completions")
AGENT_ID = os.getenv("TEST_AGENT_ID", "chaos-agent-999")

def fire_request(req_num):
    headers = {
        "Content-Type": "application/json",
        "x-internal-agent-id": AGENT_ID,
        "Authorization": "Bearer sk-sagc-chaos-test"
    }
    payload = {
        "model": "runaway-target",
        "messages": [{"role": "user", "content": "Simulate runaway loop test."}]
    }
    try:
        response = requests.post(PROXY_URL, headers=headers, json=payload, timeout=5)
        print(f"[Request {req_num:03d}] Status: {response.status_code}")
    except Exception as e:
        print(f"[Request {req_num:03d}] Error: {e}")

print("--- 🌪️ Chaos Injection: Sequential Runaway Simulation ---")
for i in range(1, 21):  # Send 20 sequential requests
    fire_request(i)
    time.sleep(0.1)     # Slight delay to prevent Uvicorn TCP dropping
