import os
import re

# Patterns to match and replace
REDACTION_MAP = {
    r"Bearer [A-Za-z0-9\-_.]+(?=\s|$)": "Bearer REDACTED_TOKEN",
    r"AIza[0-9A-Za-z-_]{35}": "GCP_API_KEY_REDACTED",
    r"projects/[0-9]+/secrets/[A-Za-z0-9-]+": "projects/PROJECT_ID/secrets/SECRET_ID",
    r"us-central1-docker\.pkg\.dev/[a-z0-9-]+/[a-z0-9-]+": "GCR_PATH_REDACTED",
    r"UPSTASH_REDIS_REST_TOKEN=[A-Za-z0-9]+": "UPSTASH_REDIS_REST_TOKEN=REDACTED",
    r"projects/[0-9]{12}/": "projects/PROJECT_NUMBER/"
}

def scrub_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for pattern, replacement in REDACTION_MAP.items():
            new_content = re.sub(pattern, replacement, new_content)
        
        # Save to a new 'scrubbed' directory to avoid overwriting your source
        output_path = os.path.join("scrubbed_for_audit", file_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    except Exception as e:
        print(f"Skipping {file_path}: {e}")

# Walk the workspace and scrub relevant files
for root, dirs, files in os.walk('.'):
    if '.git' in dirs: dirs.remove('.git')
    if 'node_modules' in dirs: dirs.remove('node_modules')
    if 'scrubbed_for_audit' in dirs: dirs.remove('scrubbed_for_audit')
    for file in files:
        if file.endswith(('.py', '.tf', '.rego', '.yaml', '.md', '.json')):
            scrub_file(os.path.join(root, file))

print("Audit bundle generated in ./scrubbed_for_audit/")
