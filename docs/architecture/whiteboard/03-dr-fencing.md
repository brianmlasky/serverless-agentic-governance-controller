# Whiteboard View 3: Multi-Cloud DR Fencing

**Purpose:** To demonstrate how the SAGC maintains financial governance during a regional cloud outage while minimizing egress latency and preventing "Split-Brain" scenarios.

## The Architectural Pillars
1. **Active-Passive Setup:** Primary (GCP) and Standby (AWS).
2. **Asynchronous State Sync:** 15-minute token-budget replication to trade off strict accuracy for sub-millisecond local latency.
3. **Quorum-Based Fencing:** The failover controller requires 3 independent regional health checks to prevent false-positive promotions.

## The Talk Track
* **Active-Passive Logic:** We utilize GCP as primary and AWS as a warm-standby to avoid the massive egress costs of active-active sync.
* **State Replication:** Token budgets replicate asynchronously every 15 minutes. We accept a maximum budget drift of 15 minutes to preserve the performance of the critical path.
* **Fencing Controller:** Monitors the GCP control plane. If a hard outage is detected, it atomicizes the DNS weight shift to AWS and promotes the AWS Redis instance to be the new source of truth.
* **Network Boundary:** AWS is pre-warmed with immutable container images so it can scale from zero to full capacity in under 5 minutes.

## Proactive Defense (The "Means Test")
**The Risk:** Split-Brain.
**The Fix:** Quorum-based heartbeats. We require confirmation from three geographically distributed monitoring nodes before triggering an automated failover, ensuring a human or automated fluke doesn't cause a double-spend event.
