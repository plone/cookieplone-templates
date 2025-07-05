### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
GIT_FOLDER=$(CURRENT_DIR)/.git

PROJECT_NAME={{ cookiecutter.__project_slug }}
STACK_NAME={{ cookiecutter.__devops_stack_name }}

PLONE_VERSION=$(shell cat backend/version.txt)

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

.PHONY: all
all: install

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

###########################################
# Backend
###########################################
.PHONY: backend-install
backend-install:  ## Create virtualenv and install Plone
	$(MAKE) -C "./backend/" install
	$(MAKE) backend-create-site

.PHONY: backend-build
backend-build:  ## Build Backend
	$(MAKE) -C "./backend/" install

.PHONY: backend-create-site
backend-create-site: ## Create a Plone site with default content
	$(MAKE) -C "./backend/" create-site

.PHONY: backend-update-example-content
backend-update-example-content: ## Export example content inside package
	$(MAKE) -C "./backend/" update-example-content

.PHONY: backend-start
backend-start: ## Start Plone Backend
	$(MAKE) -C "./backend/" start

.PHONY: backend-test
backend-test:  ## Test backend codebase
	@echo "Test backend"
	$(MAKE) -C "./backend/" test

###########################################
# Environment
###########################################
.PHONY: install
install:  ## Install
	@echo "Install Backend"
	$(MAKE) backend-install

.PHONY: clean
clean:  ## Clean installation
	@echo "Clean installation"
	$(MAKE) -C "./backend/" clean

###########################################
# QA
###########################################
.PHONY: format
format:  ## Format codebase
	@echo "Format the codebase"
	$(MAKE) -C "./backend/" format

.PHONY: lint
lint:  ## Format codebase
	@echo "Lint the codebase"
	$(MAKE) -C "./backend/" lint

.PHONY: check
check:  format lint ## Lint and Format codebase

###########################################
# i18n
###########################################
.PHONY: i18n
i18n:  ## Update locales
	@echo "Update locales"
	$(MAKE) -C "./backend/" i18n

###########################################
# Testing
###########################################
.PHONY: test
test:  backend-test ## Test codebase

###########################################
# Container images
###########################################
.PHONY: build-images
build-images:  ## Build container images
	@echo "Build"
	$(MAKE) -C "./backend/" build-image

###########################################
# Local Stack
###########################################
.PHONY: stack-create-site
stack-create-site:  ## Local Stack: Create a new site
	@echo "Create a new site in the local Docker stack"
	@echo "(Stack must not be running already.)"
	PLONE_VERSION=$(PLONE_VERSION) docker compose -f docker-compose.yml run --build backend ./docker-entrypoint.sh create-site

.PHONY: stack-start
stack-start:  ## Local Stack: Start Services
	@echo "Start local Docker stack"
	PLONE_VERSION=$(PLONE_VERSION) docker compose -f docker-compose.yml up -d --build
	@echo "Now visit: http://{{ cookiecutter.__project_slug }}.localhost"

.PHONY: stack-status
stack-status:  ## Local Stack: Check Status
	@echo "Check the status of the local Docker stack"
	@docker compose -f docker-compose.yml ps

.PHONY: stack-stop
stack-stop:  ##  Local Stack: Stop Services
	@echo "Stop local Docker stack"
	@docker compose -f docker-compose.yml stop

.PHONY: stack-rm
stack-rm:  ## Local Stack: Remove Services and Volumes
	@echo "Remove local Docker stack"
	@docker compose -f docker-compose.yml down
	@echo "Remove local volume data"
	@docker volume rm $(PROJECT_NAME)_vol-site-data
