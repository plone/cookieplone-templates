### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# Python checks
UV?=uv

# installed?
ifeq (, $(shell which $(UV) ))
  $(error "UV=$(UV) not found in $(PATH)")
endif

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

VENV_FOLDER=$(BACKEND_FOLDER)/.venv
BIN_FOLDER=$(VENV_FOLDER)/bin

# Manage Environment
ifneq ($(wildcard .env),)
include .env
export
else
$(error "Please create a .env file in the project root (use .env_dist as a base)")
endif


all: help

# Help
.PHONY: help
help: ## This help message
	@echo "----------------------------------"
	@echo "$(GREEN)Environment Variables$(RESET)"
	@echo "----------------------------------"
	@echo "- SRC_PATH: $(GREEN)$(SRC_PATH)$(RESET)"
	@echo "- DST_PATH: $(GREEN)$(DST_PATH)$(RESET)"
	@echo ""


# Installation

$(BIN_FOLDER)/transmute: ## Install dependencies
	@echo "$(GREEN)==> Install environment$(RESET)"
	@uv sync

.PHONY: install
install: $(BIN_FOLDER)/transmute ## Install package

.PHONY: clean
clean: ## Clean environment
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	rm -rf $(VENV_FOLDER) .python-version .venv .ruff_cache .pytest_cache uv.lock

# Run helper scripts
.PHONY: script-reports-to-csv
script-reports-to-csv: ## Convert reports to CSV
	@echo "📊 Converting reports"
	@uv run scripts/reports_as_csv.py

# Reports
.PHONY: report-src
report-src: ## Generate a report about the source data
	@echo "📋 Generating a report about the source data"
	@uv run transmute report $(SRC_PATH)

# Run transmute
.PHONY: transmute-no-ui
transmute-no-ui: ## Run transformation without using the graphical interface
	@echo "🚀 Run transmute"
	@uv run transmute run --no-ui --clean-up --write-report $(SRC_PATH) $(DST_PATH)

.PHONY: transmute
transmute: ## Run transformation using the graphical interface
	@echo "🚀 Run transmute"
	@uv run transmute run --clean-up --write-report $(SRC_PATH) $(DST_PATH)
