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

BIN_FOLDER = "../../bin"

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean
	rm -rf volto-addon

$(BIN_FOLDER)/cookieplone:  ## cookieplone installation
	$(MAKE) -C "../.." bin/cookieplone

.PHONY: format
format: $(BIN_FOLDER)/cookieplone ## Format code
	@echo "$(GREEN)==> Formatting codebase $(RESET)"
	$(BIN_FOLDER)/black hooks tests
	$(BIN_FOLDER)/isort hooks tests

.PHONY: generate
generate:  $(BIN_FOLDER)/cookieplone ## Create a sample package
	@echo "$(GREEN)==> Creating new test package$(RESET)"
	rm -rf volto-addon
	$(BIN_FOLDER)/cookiecutter . --no-input

.PHONY: test
test: $(BIN_FOLDER)/cookieplone ## Create a sample package and tests it
	@echo "$(GREEN)==> Creating new test package$(RESET)"
	$(BIN_FOLDER)/python -m pytest tests
