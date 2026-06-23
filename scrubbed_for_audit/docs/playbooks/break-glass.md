# Runbook: Emergency Break-Glass (Bypass SAGC)
If the SAGC Envoy proxy is dropping traffic, change `failure_mode_allow` from `false` to `true` in `k8s/policies/sidecar/envoy-ext-authz.yaml` and apply. **Post-Incident Action:** A root-cause ADR is mandatory before reverting this bypass.
