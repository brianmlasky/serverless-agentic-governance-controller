.PHONY: test-chaos install

install:
	pip install -r requirements.txt || echo "No requirements to install"

test-chaos:
	@echo "Executing Fiscal Chaos Agent..."
	@python3 tests/chaos_test_runaway.py; \
	STATUS=$$?; \
	if [ $$STATUS -eq 1 ]; then \
		echo "Verification Passed: Controller successfully executed Fail-Closed termination (exit 1)."; \
		exit 0; \
	else \
		echo "Verification Failed: Expected hard kill (exit 1), but got $$STATUS"; \
		exit 1; \
	fi
