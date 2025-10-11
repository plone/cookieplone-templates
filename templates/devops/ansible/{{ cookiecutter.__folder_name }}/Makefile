### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

ifeq ($(wildcard .env),)
$(info No .env file found, using default environment variables)
else
$(info Using environment variables from .env file)
include .env
export
endif

INSTALL_STAMP := .install.stamp

CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

VENV_DIR=$(CURRENT_DIR)/.venv
BIN_DIR=$(VENV_DIR)/bin
ROLES_DIR=$(CURRENT_DIR)/roles

.PHONY: all
all: help

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml
	@echo "🚀 Setting up devops"
	@echo "- Installing dependencies"
	@uv sync
	@echo "- Install Ansible Roles and Collections"
	@uv run ansible-galaxy install -r requirements.yml --force --no-deps
	@touch $(INSTALL_STAMP)

.PHONY: update
update: $(INSTALL_STAMP) ## Update dependencies and roles
	@echo "🚀 Update dependencies and roles"
	@uv run ansible-galaxy install -r requirements.yml --force --no-deps

.PHONY: clean
clean: ## Remove virtualenv and downloaded roles
	@echo "🚀 Cleanup the current environment"
	@rm -rf $(INSTALL_STAMP) .venv roles/*

.PHONY: lint
lint: $(INSTALL_STAMP)
	@uv run ansible-lint
