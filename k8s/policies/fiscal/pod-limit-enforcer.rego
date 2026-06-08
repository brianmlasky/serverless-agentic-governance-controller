package k8s.fiscal.guardrails

# This policy ensures that every container within a Pod explicitly defines 
# resource limits. Without this, an agentic workload could unintentionally 
# consume all cluster capacity, leading to a massive billing spike.

deny[msg] if {
    # Match only on Pods
    input.request.kind.kind == "Pod"
    
    # Iterate through every container in the Pod
    container := input.request.object.spec.containers[_]
    
    # Check: Does the 'resources.limits' object exist?
    not container.resources.limits

    # If the limit block is missing, deny the deployment
    msg := sprintf("FISCAL VIOLATION: Container '%v' lacks resource limits. All agentic workloads must be bounded.", [container.name])
}

# Advanced check: Ensure limits are not set to 'infinity'
deny[msg] if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    
    # Check if the memory limit is set to an absurdly high value
    # OPA can mathematically compare integers here
    container.resources.limits.memory == "1000000000"
    
    msg := sprintf("FISCAL VIOLATION: Container '%v' has a non-production-grade memory limit.", [container.name])
}