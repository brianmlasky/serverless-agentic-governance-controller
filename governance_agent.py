import json
import sys

def analyze_logs(log_line):
    try:
        data = json.loads(log_line)
        # Process granular tool costs
        if data.get("event") == "tool_execution":
            print(f"FISCAL: Tool '{data['tool']}' executed at cost ${data['cost_usd']:.4f}")
            
        # Process latency alerts
        if data.get("event") == "http_request" and data.get("latency_seconds", 0) > 0.5:
            print(f"ALERT: High latency on {data['path']}: {data['latency_seconds']}s")
            
    except json.JSONDecodeError:
        pass

if __name__ == "__main__":
    for line in sys.stdin:
        analyze_logs(line)
