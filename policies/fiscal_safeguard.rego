package sagc.fiscal

# Default states
default hard_kill = false
default throttle = false
default alert = false

# Business Logic: Only trigger hard kill if consumption hits 100%
hard_kill {
    input.consumption_percentage >= 100
}

# Business Logic: Throttle API calls at 90%
throttle {
    input.consumption_percentage >= 90
    input.consumption_percentage < 100
}

# Business Logic: Alert FinOps at 80%
alert {
    input.consumption_percentage >= 80
    input.consumption_percentage < 90
}
