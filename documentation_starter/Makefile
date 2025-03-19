# Makefile for testing documentation_starter template
.DEFAULT_GOAL   = help
SHELL           = bash

# Internal variables
VENV_DIR        = .venv
PYTHON          = python3
PIP             = $(VENV_DIR)/bin/pip
UV              = $(VENV_DIR)/bin/uv
PYTEST          = $(VENV_DIR)/bin/pytest
COOKIECUTTER    = $(VENV_DIR)/bin/cookiecutter
OUTPUT_DIR      = output_test
DOCS_DIR        = $(OUTPUT_DIR)/docs
SPHINXBUILD     = $(VENV_DIR)/bin/sphinx-build

# Phony targets
.PHONY: help venv test bake build-docs clean

# Help target
.PHONY: help
help:  ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Virtual environment setup
venv: $(VENV_DIR)/bin/uv  ## Set up virtual environment with uv and testing tools

$(VENV_DIR)/bin/uv:  ## Create virtual environment and install dependencies
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install uv
	$(UV) pip install pytest cookiecutter pytest-cookies

# Test target: Run pytest
test: venv  ## Run pytest tests for documentation_starter
	$(UV) pip install cookieplone
	$(PYTEST) tests/

# Bake target: Generate the template
bake: venv  ## Bake the documentation_starter template into output_test/
	rm -rf $(OUTPUT_DIR)
	$(COOKIECUTTER) . --no-input --output-dir $(OUTPUT_DIR)

# Build-docs target: Build the generated documentation
build-docs: bake  ## Build HTML documentation in the generated project
	cd $(DOCS_DIR) && $(UV) pip install -e "../.[dev]" && $(SPHINXBUILD) -b html . _build/html
	@echo "Documentation built in $(DOCS_DIR)/_build/html"

# Clean target: Remove virtual environment and output
clean:  ## Remove virtual environment and test output
	rm -rf $(VENV_DIR) $(OUTPUT_DIR)
