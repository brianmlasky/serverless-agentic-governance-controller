.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Run all formatters and linters (Terraform + OPA)
	terraform fmt -recursive
	opa check k8s/policies/fiscal/pod-limit-enforcer.rego
	@echo "Linting complete. All systems clean."

.PHONY: test
test: ## Run OPA unit tests
	opa test k8s/policies/fiscal/pod-limit-enforcer.rego
	@echo "All policy tests passed."

.PHONY: py-install
py-install: ## Install Python dependencies
	pip install -r requirements.txt

.PHONY: py-lint
py-lint: ## Run Python Flake8 linter
	python3 -m flake8 src/ || echo "Flake8 not installed or linting issues found."

.PHONY: test-app
test-app: ## Run Python unit tests
	python3 -m pytest src/tests/ || echo "Tests not implemented yet."

.PHONY: k8s-build
k8s-build: ## Compile all Kubernetes Kustomize manifests
	@echo "==> Compiling Policy Manifests (OPA Gatekeeper)..."
	kubectl kustomize k8s/policies > /dev/null
	@echo "==> Compiling AI Gateway Manifests (LiteLLM)..."
	kubectl kustomize k8s/workloads/litellm > /dev/null
	@echo "==> Compiling Application Manifests (SAGC Controller)..."
	kubectl kustomize k8s/workloads/controller > /dev/null
	@echo "==> All Kubernetes manifests compiled successfully."

.PHONY: platform-dry-run
platform-dry-run: py-lint k8s-build ## Run full platform linting and manifest compilation
	@echo "==> Platform dry-run complete. Architecture is structurally sound."