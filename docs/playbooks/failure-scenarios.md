## Scenario 01: Global Deployment Blockage (Policy False-Positive)

### Context & Risk
This scenario occurs when the `governance-controller` incorrectly identifies valid infrastructure as non-compliant. The business risk is "Deployment Paralysis," preventing the shipping of hotfixes or features. This policy exists to ensure security but can become a bottleneck if rules are too aggressive.

### 1. Detection & Alerting
*   **Monitor**: Watch the `admission_webhook_denial_rate` metric in the Dashboard.
*   **Alert**: Trigger a P1 incident if the denial rate > 50% over a 5-minute rolling window.

### 2. Triage (Blast Radius Assessment)
*   **Action**: Execute the following to identify scope:
```bash
    # Count blocked deployments by namespace
    kubectl get events --all-namespaces --sort-by='.lastTimestamp' | \
      grep AdmissionWebhook | awk '{print $1}' | sort | uniq -c | sort -rn
    ```
*   **Decision Matrix**:
*   **Single Namespace + Non-Critical**: Apply targeted policy exception for that namespace only.
*   **Single Namespace + Critical (Auth/Monitoring/Payment)**: Trigger Break-Glass immediately.
*   **Multiple Namespaces (>3)**: Trigger Break-Glass immediately.

### 3. Immediate (Break-Glass Procedure)
*   **Approval**: 
1. Post to `#security-oncall`: "@here Need approval to toggle Audit-Only mode. Incident ID: <ID>. Blast radius: <X namespaces>."
2. **SLA**: If no response in **2 minutes**, escalate to On-call Security Architect.
3. **Fallback**: On-call Platform Lead may approve if Security is unresponsive after 3 minutes.
*   **Action**: Toggle mode to restore flow:
```bash
    kubectl patch governanceconfig global-config -p '{"spec": {"mode": "Audit-Only"}}' --type=merge
    ```
*   **SLA**: `Audit-Only` mode expires in **4 hours**. Reverts automatically unless extended by Architect.

### 4. Investigation & Fix
*   **Forensic**: 
```bash
    # Extract recent denials to find the offending rule
    kubectl logs -n governance-system deployment/governance-controller --tail=500 | grep "violation" > /tmp/denials.log
    # Check policy change history
    git log --oneline -n 10 -- policies/
    ```
*   **Rollback**: Revert to the last known stable version:
```bash
    kubectl apply -f manifests/governance-config-v2.1.3-stable.yaml
    ```

### 5. Compliance & Retrospective
*   **Sign-Off**: Within 24 hours, resource owners must:
    1. **Remediate**: Fix resource to be compliant.
    2. **Exception**: File ticket with risk acceptance.
    3. **Rollback**: Delete non-compliant resource.
*   **Post-Mortem**: Mandatory review within 48h to document root cause and update test suite.

## Scenario 02: The "Runaway Environment" (Uncontrolled State Mutation)

### Context & Risk
This scenario occurs when a flawed Terraform deployment or a compromised CI/CD pipeline begins applying destructive or highly expensive infrastructure changes automatically. The immediate business risk is exponential cost overrun (budget burn) or critical infrastructure deletion. 

### 1. Detection & Alerting
* **Monitor**: Watch the Cloud Provider billing alerts and CI/CD deployment frequency metrics.
* **Alert**: Trigger a P0 incident if unexpected high-cost resources (e.g., massive GPU instances) are provisioned outside of planned maintenance windows.

### 2. Triage (Blast Radius Assessment)
* **Action**: Identify if the runaway deployment is currently active.
* **Decision**: 
    * If active: Proceed to Immediate Action (Stop the Bleeding).
    * If already completed: Proceed directly to Investigation & Fix (State Reconciliation).

### 3. Immediate Action (Stop the Bleeding)
* **CRITICAL WARNING**: Do **not** immediately trigger a code rollback in Git. An automated rollback might compound the state corruption.
* **Action**: Lock the State Backend to prevent further automated applies.
    ```bash
    # Example: Lock the HCP Terraform workspace via CLI
    terraform workspace lock <workspace-name>
    ```
* **Manual Intervention**: Manually scale down expensive instances or sever compromised network routes in the cloud console to stop immediate financial or security bleeding.

### 4. Investigation & Fix (State Reconciliation)
* **Rollback Intent**: Revert the Git commit to the last known good SHA.
* **Diff Check**: Run a plan to observe the delta between the broken reality and the reverted code.
    ```bash
    terraform plan -out=recovery.tfplan
    ```
* **State Surgery**: If the change is too complex for a standard apply, force the state back to a known good configuration without destroying valid resources.
    ```bash
    # Move or import state manually
    terraform state mv <source> <destination>
    terraform import <resource_type>.<name> <existing_id>
    ```

### 5. Compliance & Retrospective (Post-Mortem Guardrails)
* **Automated Guardrails**: Implement Policy-as-Code (OPA/Sentinel) in the CI pipeline to block expensive instance types or zero-retention periods before the `terraform apply` phase.
* **Manual Guardrails**: For Production workspaces, disable "Auto-Apply." 
* **Sign-Off**: Require explicit human-in-the-loop approval for any Terraform plans modifying sensitive resources (Databases, IAM, Networking).
