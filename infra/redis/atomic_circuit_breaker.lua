-- SAGC Atomic Fiscal Circuit Breaker
-- Executes entirely within the Redis C-engine for guaranteed linearizability
--
-- KEYS[1]: The Workload Identity token bucket (e.g., identity:sagc-agent-01:tpm)
-- ARGV[1]: The maximum allowed tokens (e.g., 10000)
-- ARGV[2]: The requested tokens for the current prompt (e.g., 200)
-- ARGV[3]: The TTL window for the circuit breaker in seconds (e.g., 60)

local token_key = KEYS[1]
local max_budget = tonumber(ARGV[1])
local requested_tokens = tonumber(ARGV[2])
local ttl_window = tonumber(ARGV[3])

-- 1. Read current state
local current_burn = redis.call("GET", token_key)
if not current_burn then
    current_burn = 0
else
    current_burn = tonumber(current_burn)
end

-- 2. Evaluate Circuit Breaker
if (current_burn + requested_tokens) > max_budget then
    -- FAIL: Budget Exceeded. Return 0 and the current burn.
    return {0, current_burn} 
else
    -- PASS: Atomically Increment Ledger
    local new_burn = redis.call("INCRBY", token_key, requested_tokens)
    
    -- If this is a fresh bucket, apply the Time-to-Live window
    if current_burn == 0 then
        redis.call("EXPIRE", token_key, ttl_window)
    end
    
    -- Return 1 (Success) and the updated burn
    return {1, new_burn}
end
