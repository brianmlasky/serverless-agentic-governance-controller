# Project Variables
APP_NAME = agentic-governance-controller
PYTHON = python3

.PHONY: help install test run clean

help: ## Show this help message
	@echo "Usage: make [target]"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	$(PYTHON) -m pip install -r requirements.txt

test: ## Run the governance logic test suite
	$(PYTHON) main.py

run: ## Start the API server locally
	$(PYTHON) -m uvicorn main:app --reload

clean: ## Clean up temporary files
	rm -rf __pycache__ .pytest_cache .venv
	@echo "Cleaned up project artifacts."

lint: ## Run basic linting (checks code style)
	@echo "Checking code style..."
	# You can add 'flake8 main.py' here if installed

check-security: ## Basic check for security issues
	@echo "Reviewing SECURITY.md protocols..."