Break-Glass Rego Policy Example

package terraform.governance

# 1. Default Policy: Fail-Closed
default allow = false

# 2. Allow if within normal budget (Normal Operation)
allow {
    not exceeds_budget
}

# 3. Allow if valid Break-Glass token exists (The Override)
allow {
    is_break_glass_active
}

# 4. Logic for Break-Glass
is_break_glass_active {
    input.oidc_claims.break_glass.active == true
    time.now_ns() < input.oidc_claims.break_glass.expiry_ns
}

#(Note: To ensure production safety, an additional explicit deny rule must be added that evaluates independently #of the allow block to prevent destructive actions—like database deletion or IAM changes—even during an active #Break-Glass window).
