import os
import sys
from google.cloud import secretmanager

def retrieve_llm_key(project_id: str, secret_id: str) -> str:
    """
    Retrieves the LLM API key from Google Secret Manager.
    This client automatically utilizes the ambient Workload Identity Federation 
    credentials injected by the GKE metadata server. No static keys are loaded.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"FATAL: Identity handshake or authorization failed: {e}")
        sys.exit(1)

def run_governance_loop():
    print("===================================================")
    print("Serverless Agentic Governance Controller Booting...")
    print("===================================================")
    
    project_id = "alert-hall-466720-c0"
    secret_id = "litellm-provider-api-key"
    
    print("1. Interrogating ambient Kubernetes identity...")
    print("2. Exchanging OIDC token with Google Secret Manager...")
    
    api_key = retrieve_llm_key(project_id, secret_id)
    
    print("3. Cryptographic payload successfully retrieved.")
    # Masking the key for security logging compliance
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "****"
    print(f"   [Token Signature: {masked_key}]")
    print("\nGovernance control loop initialized. Awaiting agentic workloads...")

if __name__ == "__main__":
    run_governance_loop()