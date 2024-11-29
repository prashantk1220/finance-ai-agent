# Variables
APP_NAME=app.main:app  # Path to FastAPI app
TEST_DIR=tests         # Directory containing test files
UVICORN_HOST=127.0.0.1
UVICORN_PORT=8000

.PHONY: help install test run clean ui

install: ## Install required Python dependencies
	pip install -r requirements.txt

test: ## Run all test cases
	pytest $(TEST_DIR)

run: ## Run the FastAPI application using Uvicorn (Ensure DB is running)
	uvicorn $(APP_NAME) --host $(UVICORN_HOST) --port $(UVICORN_PORT) --reload

ui: ## Launch the Gradio ui
	python -m ui.view

clean: ## Clean up Python cache and test artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage


help: ## Display this help message
	@echo "Usage: make [target]"
	@echo
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'
