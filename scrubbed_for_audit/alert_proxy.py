import json, os, time
from kubernetes import client, config

config.load_incluster_config()
v1 = client.CoreV1Api()
namespace = "litellm"
cm_name = "governance-commands"

def check_for_events():
    cm = v1.read_namespaced_config_map(cm_name, namespace)
    return cm.data.get("event")

print("Governance Controller Started (Polling Mode).", flush=True)
last_event = None
total_spend = 0.0

while True:
    try:
        event_str = check_for_events()
        if event_str and event_str != last_event:
            data = json.loads(event_str)
            if "cost_usd" in data:
                total_spend += data["cost_usd"]
                print(f"TRACKING: Total Spend ${total_spend:.4f}", flush=True)
                if total_spend > 1.00:
                    print(f"ACTION: Terminating litellm-gateway-trigger-pod!", flush=True)
            last_event = event_str
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(2)
