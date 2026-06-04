# Terraform Architectural Standards

## 1. State vs. Query (The Boundary of Ownership)
To maintain a resilient and modular infrastructure platform, we enforce a strict logical boundary between resources we manage and resources we reference.

* **Resources (`resource` blocks):** "I built this, I own it." 
    * Use this *only* for infrastructure that this specific state file is responsible for creating, updating, and destroying. 
    * These assets are tracked in the Terraform State.
* **Data Sources (`data` blocks):** "I am borrowing information from the world." 
    * Use this to execute live API queries against the cloud provider to fetch information about infrastructure managed elsewhere. 
    * These are *not* managed by the local state file, preventing state lock conflicts between teams.
