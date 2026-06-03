.PHONY: dev test lint format build clean

dev:
	pip install -e ".[dev]"

test:
	pytest -v

lint:
	ruff check src tests

format:
	ruff check --fix src tests

build:
	python -m build

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
