.PHONY: help install dev-install test lint format clean run docs pull-data pull-prices pull-financials

help:
	@echo "Available commands:"
	@echo ""
	@echo "  Setup:"
	@echo "    make install       - Install dependencies"
	@echo "    make dev-install   - Install development dependencies"
	@echo ""
	@echo "  Testing & Quality:"
	@echo "    make test          - Run tests with coverage"
	@echo "    make test-fast     - Quick test run"
	@echo "    make lint          - Run code linting (flake8)"
	@echo "    make format        - Format code with black"
	@echo "    make typecheck     - Run type checking with mypy"
	@echo ""
	@echo "  Data:"
	@echo "    make pull-data     - Pull VN30 data (full pipeline)"
	@echo "    make pull-prices   - Pull OHLCV prices only"
	@echo "    make pull-financials - Pull financial statements only"
	@echo "    make pull-news     - Pull news & events only"
	@echo ""
	@echo "  Documentation:"
	@echo "    make docs          - Show documentation info"
	@echo ""
	@echo "  Development:"
	@echo "    make clean         - Clean up generated files"
	@echo "    make run           - Run the application"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest --cov=src --cov-report=html --cov-report=term

test-fast:
	pytest --cov=src -q

lint:
	flake8 src/ tests/

format:
	black src/ tests/ docs/

typecheck:
	mypy src/ --ignore-missing-imports

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/
	rm -rf build/ dist/ *.egg-info/

docs:
	@echo "Documentation can be found in docs/ directory"
	@echo "See docs/README.md for more information"

run:
	python -m src.main

# Data pulling commands
pull-data:
	python run_data_puller.py

pull-prices:
	python run_data_puller.py --prices-only

pull-financials:
	python run_data_puller.py --financials-only

pull-news:
	python run_data_puller.py --news-only

pull-data-verbose:
	python run_data_puller.py -v

# Virtual environment
venv:
	python -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"
