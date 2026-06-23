import yaml
import sys
import os

def validate_config(path):
    if not os.path.exists(path):
        print(f"File {path} not found.")
        return False
    with open(path, 'r') as f:
        try:
            # 1. Load the Kubernetes ConfigMap
            k8s_config = yaml.safe_load(f)
            # 2. Extract the actual LiteLLM config string
            litellm_raw = k8s_config.get('data', {}).get('config.yaml', '')
            if not litellm_raw:
                print("Error: 'data.config.yaml' missing in ConfigMap.")
                return False
            
            # 3. Parse the nested LiteLLM configuration
            config = yaml.safe_load(litellm_raw)
            if 'model_list' not in config:
                print("Error: 'model_list' missing in LiteLLM config.")
                return False
                
            print(f"Validation successful for {path}")
            return True
        except Exception as e:
            print(f"Error parsing YAML: {e}")
            return False

if __name__ == "__main__":
    if not validate_config('terraform/k8s/litellm-config.yaml'):
        sys.exit(1)
