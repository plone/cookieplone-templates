SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

.PHONY: all
all: build

BASE_FOLDER = $(shell git rev-parse --show-toplevel)
VENV_FOLDER = ${BASE_FOLDER}/.venv
BIN_FOLDER = ${VENV_FOLDER}/bin

TEMPLATE = devops_ansible
DEVOPS_FOLDER_NAME = ansible

.PHONY: clean
clean: ## Clean
	rm -rf $(ADDON_NAME)

$(VENV_FOLDER): ## cookieplone installation
	$(MAKE) -C $(BASE_FOLDER) sync

.PHONY: format
format: $(VENV_FOLDER)## Format code
	@echo "$(GREEN)==> Formatting $(TEMPLATE) codebase $(RESET)"
	@uv run ruff format --config $(BASE_FOLDER)/pyproject.toml hooks
	@uv run ruff check --select I --fix --config $(BASE_FOLDER)/pyproject.toml hooks

.PHONY: generate
generate:  $(VENV_FOLDER) ## Create a sample package
	@echo "$(GREEN)==> Creating new test package$(RESET)"
	rm -rf $(DEVOPS_FOLDER_NAME)
	COOKIEPLONE_REPOSITORY=$(BASE_FOLDER) uv run cookieplone $(TEMPLATE) --no-input

.PHONY: test
test: $(VENV_FOLDER)## Create a sample package and tests it
	@echo "$(GREEN)==> Creating new test package$(RESET)"
	@uv run pytest $(BASE_FOLDER)/tests/templates/devops/ansible

.PHONY: test-pdb
test-pdb: $(VENV_FOLDER)## Stop on the first failed test
	@echo "$(GREEN)==> Test template, stop on first error$(RESET)"
	@uv run pytest $(BASE_FOLDER)/tests/templates/devops/ansible -x --pdb
