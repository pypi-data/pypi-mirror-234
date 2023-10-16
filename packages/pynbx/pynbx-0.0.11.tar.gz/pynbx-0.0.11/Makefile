PIP=pip
SHELL=/bin/bash

setup-dev:
	${PIP} install -e .[dev]

lint:
	flake8 .

format:
	isort . && black .

test-gate:
	pip install .[dev]
	cd tests && pytest

test-nightly:
	pip install .[dev]
	cd tests && pytest
