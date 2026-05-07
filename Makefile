PYTHON ?= python3

.PHONY: install bootstrap test validate doctor

install:
	$(PYTHON) -m pip install -e ".[dev]"

bootstrap:
	cp -n .env.example .env || true
	cp -n config.example.yaml config.yaml || true

test:
	pytest -q

validate:
	ato-skill-ado-cli validate

doctor:
	ato-skill-ado-cli doctor
