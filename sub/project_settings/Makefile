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

TEMPLATE = $(shell basename $(CURRENT_DIR))
PROJECT_FOLDER_NAME = project-title
BASE_FOLDER = ../../
BIN_FOLDER = ${BASE_FOLDER}/bin


# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean
	rm -rf volto-addon

$(BIN_FOLDER)/cookieplone:  ## cookieplone installation
	$(MAKE) -C $(BASE_FOLDER) bin/cookieplone

.PHONY: format
format: $(BIN_FOLDER)/cookieplone ## Format code
	@echo "$(GREEN)==> Formatting codebase $(RESET)"
	$(BIN_FOLDER)/black hooks tests
	$(BIN_FOLDER)/isort hooks tests

.PHONY: generate
generate:  $(BIN_FOLDER)/cookieplone ## Create a sample package
	@echo "$(GREEN)==> Creating new test package$(RESET)"
	rm -rf $(PROJECT_FOLDER_NAME)
	COOKIEPLONE_REPOSITORY=$(BASE_FOLDER) $(BIN_FOLDER)/cookieplone $(TEMPLATE) --no_input

.PHONY: test
test: $(BIN_FOLDER)/cookieplone ## Create a sample package and tests it
	@echo "$(GREEN)==> Test template$(RESET)"
	$(BIN_FOLDER)/python -m pytest tests

.PHONY: test-pdb
test-pdb: $(BIN_FOLDER)/cookieplone ## Stop on the first failed test
	@echo "$(GREEN)==> Test template, stop on first error$(RESET)"
	$(BIN_FOLDER)/python -m pytest tests -x --pdb
