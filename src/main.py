import os
import sys
import time
from google.cloud import secretmanager

def retrieve_llm_key(project_id: str, secret_id: str) -> str:
    """Retrieves the LLM API key via ambient WIF credentials."""
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
    
    # Using the project variables from your architectural boundary
    project_id = "alert-hall-466720-c0"
    secret_id = "litellm-provider-api-key"
    
    print("1. Interrogating ambient Kubernetes identity...")
    api_key = retrieve_llm_key(project_id, secret_id)
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "****"
    print(f"2. Cryptographic payload retrieved. [Token: {masked_key}]")
    
    print("\n[FISCAL SECOPS] Initializing active token burn telemetry...")
    
    # Mock Fiscal Guardrails
    budget_limit = 500  # Maximum allowed spend in dollars
    current_spend = 0
    
    while True:
        time.sleep(3) # Simulate a 3-second polling cycle
        burn_rate = 125 # Simulate an aggressive agent consuming tokens
        current_spend += burn_rate
        
        print(f"   [METRIC] Current Agentic Spend: ${current_spend} / ${budget_limit} Limit")
        
        if current_spend >= budget_limit:
            print("\n🚨 CRITICAL: FISCAL CIRCUIT BREAKER TRIPPED 🚨")
            print("Policy: Fail-Closed enforcement engaged.")
            print("Action: Terminating agentic workload to prevent budget overrun.")
            sys.exit(1) # This crash tells Kubernetes the pod failed, enforcing the boundary

if __name__ == "__main__":
    run_governance_loop()