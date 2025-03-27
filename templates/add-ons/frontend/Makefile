SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

BASE_FOLDER = $(shell git rev-parse --show-toplevel)
VENV_FOLDER = ${BASE_FOLDER}/.venv
BIN_FOLDER = ${VENV_FOLDER}/bin

TEMPLATE = frontend_addon
ADDON_FOLDER_NAME = collective.addon
ADDON_FOLDER_NAME = volto-add-on

.PHONY: all
all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean
	rm -rf $(ADDON_NAME)

$(VENV_FOLDER):  ## cookieplone installation
	$(MAKE) -C $(BASE_FOLDER) sync

.PHONY: format
format: $(VENV_FOLDER) ## Format code
	@echo "$(GREEN)==> Formatting $(TEMPLATE) codebase $(RESET)"
	@uv run ruff format --config $(BASE_FOLDER)/pyproject.toml hooks
	@uv run ruff check --select I --fix --config $(BASE_FOLDER)/pyproject.toml hooks

.PHONY: generate
generate:  $(VENV_FOLDER) ## Create a sample package
	@echo "$(GREEN)==> Creating new test package$(RESET)"
	rm -rf $(ADDON_FOLDER_NAME)
	COOKIEPLONE_REPOSITORY=$(BASE_FOLDER) uv run cookieplone $(TEMPLATE) --no-input

.PHONY: test
test: $(VENV_FOLDER)## Create a sample package and tests it
	@echo "$(GREEN)==> Creating new test package$(RESET)"
	@uv run pytest $(BASE_FOLDER)/tests/templates/add-ons/frontend

.PHONY: test-pdb
test-pdb: $(VENV_FOLDER)## Stop on the first failed test
	@echo "$(GREEN)==> Test template, stop on first error$(RESET)"
	@uv run pytest $(BASE_FOLDER)/tests/templates/add-ons/frontend -x --pdb
