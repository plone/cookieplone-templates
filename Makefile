SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

.PHONY: all
all: bin/cookieplone

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean
	rm -rf bin include lib lib64 pyvenv.cfg .Python

bin/cookieplone: ## Create virtualenv and install dependencies
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install pip --upgrade
	bin/pip install -r requirements.txt --upgrade

.PHONY: format
format: bin/cookieplone ## Format code
	@echo "$(GREEN)==> Formatting codebase $(RESET)"
	bin/black hooks .scripts
	bin/isort hooks .scripts
	$(MAKE) -C "./backend_addon/" format
	$(MAKE) -C "./frontend_addon/" format
	$(MAKE) -C "./sub/frontend_project/" format

.PHONY: test
test: bin/cookieplone ## Test all cookiecutters
	@echo "$(GREEN)==> Test all cookiecutters$(RESET)"
	$(MAKE) -C "./backend_addon/" test
	$(MAKE) -C "./frontend_addon/" test
	$(MAKE) -C "./sub/frontend_project/" test

.PHONY: report-context
report-context: bin/cookieplone ## Generate a report of all context options
	@echo "$(GREEN)==> Generate a report of all context options$(RESET)"
	bin/python .scripts/report_context.py

.PHONY: report-keys-usage
report-keys-usage: bin/cookieplone ## Generate a report of usage of context keys
	@echo "$(GREEN)==> Generate a report of usage of context keys$(RESET)"
	bin/python .scripts/report_keys_usage.py
