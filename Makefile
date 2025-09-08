SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

TOP_LEVEL_TEMPLATES = add-ons/backend add-ons/frontend projects/monorepo projects/classic
SUB_TEMPLATES = sub/cache sub/frontend_project sub/project_settings

# Python checks
UV?=uv

# installed?
ifeq (, $(shell which $(UV) ))
  $(error "UV=$(UV) not found in $(PATH)")
endif

VENV_FOLDER=$(CURRENT_DIR)/.venv
BIN_FOLDER=$(VENV_FOLDER)/bin
TEMPLATES_FOLDER=$(CURRENT_DIR)/templates

.PHONY: all
all: $(VENV_FOLDER)

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean
	rm -rf bin include lib lib64 pyvenv.cfg .Python .venv

$(VENV_FOLDER): ## Create virtualenv and install dependencies
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	@uv sync

.PHONY: install
install: $(VENV_FOLDER)

.PHONY: sync
sync: ## Sync dependencies
	@echo "$(GREEN)==> Sync dependencies$(RESET)"
	@uv sync

.PHONY: format
format: $(VENV_FOLDER) ## Format code
	@echo "$(GREEN)==> Formatting codebase $(RESET)"
	@uv run ruff format hooks .scripts tests
	@uv run ruff check --select I --fix hooks .scripts tests
	$(MAKE) format_templates

.PHONY: format_templates
format_templates: $(VENV_FOLDER) ## Format code
	@echo "$(GREEN)==> Formatting templates $(RESET)"
	$(foreach project,$(TOP_LEVEL_TEMPLATES),$(MAKE) -C "$(TEMPLATES_FOLDER)/$(project)/" format ;)
	@echo "$(GREEN)==> Formatting sub-templates $(RESET)"
	$(foreach project,$(SUB_TEMPLATES),$(MAKE) -C "$(TEMPLATES_FOLDER)/$(project)/" format ;)

.PHONY: lint
lint: $(VENV_FOLDER) ## Lint code
	@echo "$(GREEN)==> Lint codebase $(RESET)"
	@uv run ruff check hooks .scripts tests

.PHONY: test
test: $(VENV_FOLDER) ## Test all cookiecutters
	@echo "$(GREEN)==> Test all cookiecutters$(RESET)"
	@uv run pytest tests

.PHONY: test-pdb
test-pdb: $(VENV_FOLDER) ## Test all cookiecutters (and stop on error)
	@echo "$(GREEN)==> Test all cookiecutters (and stop on error)$(RESET)"
	@uv run pytest tests -x --pdb

.PHONY: report-context
report-context: $(VENV_FOLDER) ## Generate a report of all context options
	@echo "$(GREEN)==> Generate a report of all context options$(RESET)"
	@uv run .scripts/report_context.py

.PHONY: report-keys-usage
report-keys-usage: $(VENV_FOLDER) ## Generate a report of usage of context keys
	@echo "$(GREEN)==> Generate a report of usage of context keys$(RESET)"
	@uv run .scripts/report_keys_usage.py

