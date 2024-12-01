.PHONY: help install test run clean ui all

# Variables
VENV_DIR=venv
APP_NAME=app.main:app  # Path to FastAPI app
UVICORN=$(VENV_DIR)/bin/uvicorn
UVICORN_HOST=127.0.0.1
UVICORN_PORT=8000
TEST_DIR=tests
PIP=$(VENV_DIR)/bin/pip
PYTEST=$(VENV_DIR)/bin/pytest
PYTHON=$(VENV_DIR)/bin/python


install: ## Install required Python dependencies into {VENV_DIR}
	python3 -m venv $(VENV_DIR)
	$(PIP) install -r requirements.txt

test: ## Run all test cases
	$(PYTEST) $(TEST_DIR)

run: ## Run the FastAPI application using Uvicorn (Ensure DB is running)
	$(UVICORN) $(APP_NAME) --host $(UVICORN_HOST) --port $(UVICORN_PORT) --timeout-keep-alive 60

all: install test run  ## Executes all the build test and run

ui: ## Launch the Gradio ui
	$(PYTHON) -m ui.view

clean: ## Clean up Python cache and test artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage

clean-all: clean ## Clean up Python cache and installed deps
	rm -rf venv


help: ## Display this help message
	@echo "Usage: make [target]"
	@echo
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'
