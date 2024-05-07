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


# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean
	rm -rf collective.addon

../bin/cookieplone:  ## cookieplone installation
	$(MAKE) -C ".." bin/cookieplone

.PHONY: format
format: ../bin/cookieplone ## Format code
	@echo "$(GREEN)==> Formatting codebase $(RESET)"
	../bin/black hooks tests
	../bin/isort hooks tests

.PHONY: generate
generate:  ../bin/cookieplone ## Create a sample package
	@echo "$(GREEN)==> Creating new test package$(RESET)"
	rm -rf collective.addon
	../bin/cookieplone . --no-input

.PHONY: test
test: ../bin/cookieplone ## Create a sample package and tests it
	@echo "$(GREEN)==> Creating new test package$(RESET)"
	../bin/python -m pytest tests
