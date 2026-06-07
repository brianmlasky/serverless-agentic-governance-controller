# Runbook 001: Orchestrated Cleanup of Orphaned GKE Resources

## Context
When a GKE Autopilot cluster is forcefully destroyed via Terraform (`terraform destroy`) without first cordoning and draining the Kubernetes workloads, GKE's native integration with Google Cloud APIs is severed prematurely. This results in "Ghost Resources"—infrastructure components that physically exist in GCP but are absent from the Terraform state file. 

These resources act as anchors, physically preventing the deletion of the underlying VPC network.

## Symptoms
A `terraform destroy` pipeline fails with errors indicating the VPC is still in use by:
* `firewalls/allow-health-check-to-pods`
* `firewalls/allow-gcp-lb-healthchecks`
* `networkEndpointGroups/k8s1-...`

## Remediation Playbook

### Phase 1: Clear Ingress Firewalls
GKE automatically injects health check firewalls for its managed Load Balancers. These must be deleted manually via the CLI:
```bash
gcloud compute firewall-rules delete allow-health-check-to-pods --quiet
gcloud compute firewall-rules delete allow-gcp-lb-healthchecks --quiet