.PHONY: test-chaos install

install:
	pip install -r requirements.txt || echo "No requirements to install"

test-chaos:
	@echo "Executing Fiscal Chaos Agent..."
	python3 tests/chaos_test_runaway.py
