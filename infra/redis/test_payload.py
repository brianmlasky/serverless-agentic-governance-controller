import urllib.request
import json
import time
from urllib.error import HTTPError, URLError

url = "http://127.0.0.1:4000/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": "Bearer sk-1234"}
payload = {"model": "runaway-target", "messages": [{"role": "user", "content": "Fiscal SecOps atomic state proxy test."}], "user": "sagc-agent-01", "max_tokens": 100}
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)

print("Polling for proxy initialization...")
for _ in range(15):
    try:
        with urllib.request.urlopen(req) as response:
            print("\n[SUCCESS] Proxy processed request and recorded burn to Redis.")
            break
    except URLError as e:
        time.sleep(2)
    except HTTPError as e:
        print(f"\n[FAILURE] HTTP {e.code}: {e.read().decode('utf-8')}")
        break
else:
    print("\n[FAILURE] Proxy never came online.")
