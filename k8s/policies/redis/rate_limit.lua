local key = KEYS[1]
local limit = tonumber(ARGV[1])
local expire_time = tonumber(ARGV[2])
local current = tonumber(redis.call('get', key) or "0")
if current + 1 > limit then
    return 0
else
    redis.call('INCR', key)
    if current == 0 then
        redis.call('EXPIRE', key, expire_time)
    end
    return 1
end
