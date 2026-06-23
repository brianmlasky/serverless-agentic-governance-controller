# Playbook 001: Triage & Incident Response

## Incident Declaration Criteria
An incident is declared when the LiteLLM proxy error budget drops below 10%, or when the Terraform CI/CD pipeline fails on `main` for more than 15 minutes.

## Runbook: GKE Workload Identity Authorization Failures
**Symptoms:** LiteLLM pods report `403 Forbidden` when attempting to read from Secret Manager.
**Mitigation Steps:**
1. Verify the Kubernetes Service Account (KSA) annotation:
   `kubectl get sa litellm-ksa -o yaml`
2. Validate the GCP IAM binding:
   `gcloud iam service-accounts get-iam-policy litellm-wif-sa@alert-hall-466720-c0.iam.gserviceaccount.com`
3. Restart the deployment to force a token refresh:
   `kubectl rollout restart deployment/litellm -n governance`

## Runbook: Terraform State Lock Contention
**Symptoms:** GitHub Actions pipeline hangs on `Acquiring state lock`.
**Mitigation Steps:**
1. Identify the stale lock ID from the GitHub Actions console.
2. Force unlock the state (Requires Principal Approval):
   `terraform force-unlock <LOCK_ID>`