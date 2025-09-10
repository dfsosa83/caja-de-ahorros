# Makefile for Income Estimator ML project

.PHONY: help install install-dev test test-cov lint format type-check security clean build docker-build docker-run docs serve train predict

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  type-check   - Run type checking"
	@echo "  security     - Run security checks"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"
	@echo "  docs         - Generate documentation"
	@echo "  serve        - Start API server"
	@echo "  train        - Train models"
	@echo "  predict      - Make predictions"

# Installation
install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

test-unit:
	pytest tests/unit/ -v

test-api:
	pytest tests/api/ -v

test-integration:
	pytest tests/integration/ -v

# Code quality
lint:
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

security:
	bandit -r src/ -f json

# Cleaning
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# Building
build: clean
	python -m build

# Docker
docker-build:
	docker build -t income-estimator-ml .

docker-run:
	docker run -p 8000:8000 income-estimator-ml

docker-dev:
	docker-compose --profile dev up -d

docker-prod:
	docker-compose up -d income-estimator-api

docker-monitoring:
	docker-compose --profile monitoring up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f income-estimator-api

# Documentation
docs:
	@echo "API documentation available at http://localhost:8000/docs when server is running"

# Application commands
serve:
	income-estimator serve

serve-dev:
	income-estimator serve --reload --log-level debug

train:
	income-estimator train

train-fast:
	income-estimator train --no-tune

predict:
	income-estimator predict

list-models:
	income-estimator list-models

# Environment setup
setup-conda:
	conda env create -f environment.yml
	conda activate income-estimator-ml

setup-venv:
	python -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	source venv/bin/activate && pip install -e .

# Data operations
download-data:
	@echo "Add commands to download sample data here"

validate-data:
	@echo "Add data validation commands here"

# CI/CD helpers
ci-test: install-dev lint type-check security test-cov

pre-commit-all:
	pre-commit run --all-files

# Jupyter
jupyter:
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

jupyter-docker:
	docker-compose --profile dev up -d jupyter
