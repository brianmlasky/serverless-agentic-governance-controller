import os
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: f.write(content.strip() + "\\n")
rbac = """
apiVersion: v1
kind: ServiceAccount
metadata:
  name: sagc-controller-sa
  namespace: sagc
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: llm-gateway-sa
  namespace: sagc
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: sagc-strict-isolation
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: sagc-isolation-binding
  namespace: sagc
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: sagc-strict-isolation
subjects:
- kind: ServiceAccount
  name: sagc-controller-sa
  namespace: sagc
- kind: ServiceAccount
  name: llm-gateway-sa
  namespace: sagc
"""
net = """
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: enforce-opa-sidecar-routing
  namespace: sagc
spec:
  podSelector:
    matchLabels:
      app: llm-gateway
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: controller
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: controller
"""
write_file("k8s/security/01-identity-rbac.yaml", rbac)
write_file("k8s/policies/network/enforce-sidecar.yaml", net)
b = "# SAGC Production Certification Bundle\\n\\n"
for t, p in [("src/security.py (F1)", "src/security.py"), ("src/main.py (F2 & F3)", "src/main.py"), ("k8s/security/01-identity-rbac.yaml (F4 Part 1)", "k8s/security/01-identity-rbac.yaml"), ("k8s/policies/network/enforce-sidecar.yaml (F4 Part 2)", "k8s/policies/network/enforce-sidecar.yaml")]:
    b += f"## {t}\\n```\\n"
    with open(p, "r") as f: b += f.read()
    b += "\\n```\\n\\n"
write_file("final_signoff_bundle.md", b)
