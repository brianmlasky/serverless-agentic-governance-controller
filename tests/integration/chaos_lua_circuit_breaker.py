import redis
import concurrent.futures
import time

# Connect to local test Redis
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# Load the Lua script from our infra directory
with open('/workspaces/serverless-agentic-governance-controller/infra/redis/atomic_circuit_breaker.lua', 'r') as f:
    lua_script = f.read()
circuit_breaker = r.register_script(lua_script)

BUDGET = 1000
COST_PER_PROMPT = 200
AGENT_ID = "identity:chaos-agent:tpm"
r.delete(AGENT_ID)

print(f"--- SAGC Concurrency Chaos Test ---")
print(f"Max Budget: {BUDGET} tokens | Cost per thread: {COST_PER_PROMPT} tokens")
print(f"Expected behavior: Exactly 5 threads should succeed. The rest MUST fail.\n")

success_count = 0
fail_count = 0

def fire_agent_request(thread_id):
    # Keys: [Agent ID], Args: [Max Budget, Request Cost, TTL]
    result = circuit_breaker(keys=[AGENT_ID], args=[BUDGET, COST_PER_PROMPT, 60])
    status = result[0]
    return status

# Fire 50 concurrent threads simultaneously
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(fire_agent_request, i) for i in range(50)]
    for future in concurrent.futures.as_completed(futures):
        if future.result() == 1:
            success_count += 1
        else:
            fail_count += 1

final_burn = r.get(AGENT_ID)
print(f"RESULTS:")
print(f"✅ Successful Requests (Permitted): {success_count}")
print(f"❌ Failed Requests (429 Dropped): {fail_count}")
print(f"🔥 Final Token Burn in Ledger: {final_burn} / {BUDGET}")

if success_count == 5 and int(final_burn) == BUDGET:
    print("\n[VERIFIED] NO DOUBLE-SPEND DETECTED. ATOMIC LUA CIRCUIT BREAKER IS OPERATIONAL.")
else:
    print("\n[FAILED] RACE CONDITION DETECTED.")
