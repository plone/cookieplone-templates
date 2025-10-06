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

REPOSITORY_SETTINGS := $(shell uvx repoplone settings dump)

PLONE_VERSION := $(shell echo '$(REPOSITORY_SETTINGS)' | jq -r '.backend.base_package_version')

IMAGE_NAME_PREFIX={{ cookiecutter.__container_image_prefix }}
IMAGE_TAG=latest

# Python checks
UV?=uv

# installed?
ifeq (, $(shell which $(UV) ))
  $(error "UV=$(UV) not found in $(PATH)")
endif

PLONE_SITE_ID=Plone
BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PLONE_VERSION=$(shell cat $(BACKEND_FOLDER)/version.txt)
EXAMPLE_CONTENT_FOLDER=${BACKEND_FOLDER}/src/{{ cookiecutter.__package_path }}/setuphandlers/examplecontent
PACKAGE_NAME := $(shell echo '$(REPOSITORY_SETTINGS)' | jq -r '.backend.name')

VENV_FOLDER=$(BACKEND_FOLDER)/.venv
export VIRTUAL_ENV=$(VENV_FOLDER)
BIN_FOLDER=$(VENV_FOLDER)/bin

# Environment variables to be exported
export PYTHONWARNINGS := ignore
export DOCKER_BUILDKIT := 1

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: debug-settings
debug-settings:  ## Debug settings
	@echo "PLONE_VERSION: $(PLONE_VERSION)"

.PHONY: sync
sync: ## Sync project dependencies
	@echo "$(GREEN)==> Sync project dependencies$(RESET)"
	@uvx repoplone deps upgrade $(PLONE_VERSION)
	@uv sync

.PHONY: install
install: sync config ## Install Plone and dependencies

instance/etc/zope.ini instance/etc/zope.conf: instance.yaml ## Create instance configuration
	@echo "$(GREEN)==> Create instance configuration$(RESET)"
	@uvx cookiecutter -f --no-input -c 2.1.1 --config-file instance.yaml gh:plone/cookiecutter-zope-instance

.PHONY: config
config: instance/etc/zope.ini

.PHONY: clean
clean: ## Clean installation and instance
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	@rm -rf $(VENV_FOLDER) pyvenv.cfg .installed.cfg instance .venv .pytest_cache .ruff_cache constraints* requirements*

.PHONY: remove-data
remove-data: ## Remove all content
	@echo "$(RED)==> Removing all content$(RESET)"
	rm -rf $(VENV_FOLDER) instance/var

.PHONY: start
start: $(VENV_FOLDER) instance/etc/zope.ini ## Start a Plone instance on localhost:8080
	@uv run runwsgi instance/etc/zope.ini

.PHONY: console
console: $(VENV_FOLDER) instance/etc/zope.ini ## Start a console into a Plone instance
	@uv run zconsole debug instance/etc/zope.conf

.PHONY: create-site
create-site: $(VENV_FOLDER) instance/etc/zope.ini ## Create a new site from scratch
	@uv run zconsole run instance/etc/zope.conf ./scripts/create_site.py

# Example Content
.PHONY: update-example-content
update-example-content: $(VENV_FOLDER) ## Export example content inside package
	@echo "$(GREEN)==> Export example content into $(EXAMPLE_CONTENT_FOLDER) $(RESET)"
	if [ -d $(EXAMPLE_CONTENT_FOLDER)/content ]; then rm -r $(EXAMPLE_CONTENT_FOLDER)/* ;fi
	@uv run plone-exporter instance/etc/zope.conf $(PLONE_SITE_ID) $(EXAMPLE_CONTENT_FOLDER)

# QA
.PHONY: lint
lint: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Lint codebase$(RESET)"
	@uvx ruff@latest check --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx pyroma@latest -d .
	@uvx check-python-versions@latest .
	@uvx zpretty@latest --check src

.PHONY: format
format: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	@uvx ruff@latest check --select I --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx ruff@latest format --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx zpretty@latest -i src

# i18n
.PHONY: i18n
i18n: $(VENV_FOLDER) ## Update locales
	@echo "$(GREEN)==> Updating locales$(RESET)"
	@uv run python -m $(PACKAGE_NAME).locales

# Tests
.PHONY: test
test: $(VENV_FOLDER) ## run tests
	@uv run pytest

.PHONY: test-coverage
test-coverage: $(VENV_FOLDER) ## run tests with coverage
	@uv run pytest --cov=$(PACKAGE_NAME) --cov-report term-missing

# Build Docker images
.PHONY: build-image
build-image:  ## Build Docker Images
	@docker build . -t $(IMAGE_NAME_PREFIX)-backend:$(IMAGE_TAG) --progress plain -f Dockerfile

# Acceptance tests
.PHONY: acceptance-backend-start
acceptance-backend-start: ## Start backend acceptance server
	ZSERVER_HOST=0.0.0.0 ZSERVER_PORT=55001 LISTEN_PORT=55001 APPLY_PROFILES="{{ cookiecutter.python_package_name }}:default" CONFIGURE_PACKAGES="plone.restapi,plone.volto,plone.volto.cors,{{ cookiecutter.python_package_name }}" $(BIN_FOLDER)/robot-server plone.app.robotframework.testing.VOLTO_ROBOT_TESTING

.PHONY: acceptance-image-build
acceptance-image-build:  ## Build Docker Images
	@docker build . -t $(IMAGE_NAME_PREFIX)-backend-acceptance:$(IMAGE_TAG) -f Dockerfile.acceptance --build-arg PLONE_VERSION=$(PLONE_VERSION)

## Add bobtemplates features (check bobtemplates.plone's documentation to get the list of available features)
add: $(VENV_FOLDER)
	@uvx plonecli add -b .mrbob.ini $(filter-out $@,$(MAKECMDGOALS))
