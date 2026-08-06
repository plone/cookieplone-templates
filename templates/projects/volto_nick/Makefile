SHELL := /bin/bash
CURRENT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`

.PHONY: all
all: test

.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean generated sample project
	rm -rf plone

.PHONY: format
format: ## Format Python helpers and tests
	@echo "$(GREEN)==> Formatting codebase $(RESET)"
	uvx ruff format hooks tests
	uvx ruff check --select I --fix hooks tests

.PHONY: test
test: ## Run template tests
	@echo "$(GREEN)==> Running tests$(RESET)"
	uv run pytest tests
