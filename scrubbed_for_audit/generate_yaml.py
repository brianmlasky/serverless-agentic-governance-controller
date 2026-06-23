import yaml

configs = {
    "api-gateway.yaml": {"name": "api-gateway", "kind": "Deployment", "image": "GCR_PATH_REDACTED/api-gateway:v2.1.0-6130474"},
    "database.yaml": {"name": "postgres-db", "kind": "StatefulSet", "image": "postgres:15"},
    "deployment.yaml": {"name": "litellm-gateway", "kind": "Deployment", "image": "docker.io/litellm/litellm:v1.84.0"}
}

for filename, info in configs.items():
    manifest = {
        "apiVersion": "apps/v1",
        "kind": info["kind"],
        "metadata": {
            "name": info["name"],
            "namespace": "litellm",
            "labels": {"cost-center": "research-dev"},
            "annotations": {"iam.gke.io/gcp-service-account": "litellm-sa@alert-hall-466720-c0.iam.gserviceaccount.com"}
        },
        "spec": {
            "selector": {"matchLabels": {"app": info["name"]}},
            "template": {
                "metadata": {
                    "labels": {"app": info["name"], "cost-center": "research-dev"},
                    "annotations": {"iam.gke.io/gcp-service-account": "litellm-sa@alert-hall-466720-c0.iam.gserviceaccount.com"}
                },
                "spec": {
                    "serviceAccountName": "litellm-sa",
                    "containers": [{"name": info["name"].split('-')[0], "image": info["image"], "securityContext": {"privileged": False}}]
                }
            }
        }
    }
    with open(f"k8s/litellm/{filename}", "w") as f:
        yaml.dump(manifest, f)
