PYTHON ?= python3

.PHONY: install setup bootstrap test validate doctor

install:
	./scripts/install.sh

setup:
	./scripts/setup.sh

bootstrap:
	cp -n .env.example .env || true
	cp -n config.example.yaml config.yaml || true

test:
	pytest -q

validate:
	ato-skill-ado-cli validate

doctor:
	@if [ -x .venv/bin/ato-skill-ado-cli ]; then \
		.venv/bin/ato-skill-ado-cli doctor; \
	else \
		ato-skill-ado-cli doctor; \
	fi
