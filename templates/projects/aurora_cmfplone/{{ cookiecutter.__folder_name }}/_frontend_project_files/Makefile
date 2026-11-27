### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-eu -o pipefail -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Recipe snippets for reuse

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

REPOSITORY_SETTINGS := $(shell uvx repoplone settings dump)

# The version of @plone/aurora that the app depends on
AURORA_VERSION := $(shell jq -r '.dependencies["@plone/aurora"]' $(CURRENT_DIR)/package.json)
PLONE_VERSION := $(shell echo '$(REPOSITORY_SETTINGS)' | jq -r '.backend.base_package_version')

DOCKER_IMAGE=plone/server-dev:${PLONE_VERSION}
DOCKER_IMAGE_ACCEPTANCE=plone/server-acceptance:${PLONE_VERSION}

ADDON_NAME := $(shell jq -r '.name' $(CURRENT_DIR)/packages/{{ cookiecutter.frontend_addon_name | unscoped_package_name }}/package.json)
IMAGE_NAME_PREFIX := $(shell echo '$(REPOSITORY_SETTINGS)' | jq -r '.container_images_prefix')
IMAGE_NAME_SEPARATOR := {{ cookiecutter.__container_registry_prefix_separator }}
IMAGE_NAME_PREFIX_WITH_SEPARATOR := $(IMAGE_NAME_PREFIX)$(IMAGE_NAME_SEPARATOR)

IMAGE_NAME=$(IMAGE_NAME_PREFIX_WITH_SEPARATOR)frontend
IMAGE_TAG=latest

.PHONY: help
help: ## Show this help
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

.PHONY: debug-settings
debug-settings:  ## Debug settings
	@echo "AURORA_VERSION: $(AURORA_VERSION)"
	@echo "PLONE_VERSION: $(PLONE_VERSION)"
	@echo "ADDON_NAME: $(ADDON_NAME)"
	@echo "IMAGE_NAME: $(IMAGE_NAME)"

# Dev Helpers
.PHONY: clean
clean: ## Clean environment
	@echo "$(RED)==> Cleaning node_modules and the build$(RESET)"
	rm -rf node_modules build .react-router .plone

.PHONY: install
install: ## Installs the project frontend in a development environment
	@echo "$(GREEN)Install$(RESET)"
	pnpm install

.PHONY: start
start: ## Starts Aurora, allowing reloading of the add-on during development
	pnpm start

.PHONY: build
build: ## Build a production bundle of the project
	pnpm build

.PHONY: i18n
i18n: ## Sync i18n
	pnpm --filter $(ADDON_NAME) i18n

.PHONY: ci-i18n
ci-i18n: ## Check if i18n is not synced
	pnpm --filter $(ADDON_NAME) i18n && git diff -G'^[^\"POT]' --exit-code

.PHONY: format
format: ## Format codebase
	pnpm prettier:fix
	pnpm lint:fix
	pnpm stylelint:fix

.PHONY: lint
lint: ## Lint, or catch and remove problems, in code base
	pnpm lint
	pnpm prettier
	pnpm stylelint --allow-empty-input

.PHONY: release
release: ## Release the add-on on npmjs.org
	pnpm release

.PHONY: release-dry-run
release-dry-run: ## Dry-run the release of the add-on on npmjs.org
	pnpm release

.PHONY: test
test: ## Run unit tests
	pnpm test

.PHONY: ci-test
ci-test: ## Run unit tests in CI
	CI=1 pnpm test

.PHONY: backend-docker-start
backend-docker-start:	## Starts a Docker-based backend for development
	@echo "$(GREEN)==> Start Docker-based Plone Backend$(RESET)"
	docker run -it --rm --name=backend -p 8080:8080 -e SITE=Plone $(DOCKER_IMAGE)

## Storybook
.PHONY: storybook-start
storybook-start: ## Start Storybook server on port 6006
	@echo "$(GREEN)==> Start Storybook$(RESET)"
	pnpm run storybook

.PHONY: storybook-build
storybook-build: ## Build Storybook
	@echo "$(GREEN)==> Build Storybook$(RESET)"
	mkdir -p $(CURRENT_DIR)/.storybook-build
	pnpm run storybook-build -o $(CURRENT_DIR)/.storybook-build

## Acceptance
.PHONY: acceptance-frontend-dev-start
acceptance-frontend-dev-start: ## Start acceptance frontend in development mode
	PLONE_API_PATH=http://127.0.0.1:55001/plone pnpm start

.PHONY: acceptance-frontend-prod-start
acceptance-frontend-prod-start: ## Start acceptance frontend in production mode
	pnpm build && PLONE_API_PATH=http://127.0.0.1:55001/plone pnpm start:prod

.PHONY: acceptance-backend-start
acceptance-backend-start: ## Start backend acceptance server
	docker run -it --rm -p 55001:55001 $(DOCKER_IMAGE_ACCEPTANCE)

.PHONY: ci-acceptance-backend-start
ci-acceptance-backend-start: ## Start backend acceptance server in headless mode for CI
	docker run -i --rm -p 55001:55001 $(DOCKER_IMAGE_ACCEPTANCE)

## Acceptance tests (Playwright)
.PHONY: install-acceptance
install-acceptance: ## Install the Playwright browsers used by the acceptance tests
	pnpm exec playwright install --with-deps chromium

.PHONY: acceptance-test
acceptance-test: ## Start the acceptance tests in interactive (UI) mode
	pnpm exec playwright test --ui

.PHONY: ci-acceptance-test
ci-acceptance-test: ## Run the acceptance tests in headless mode for CI
	pnpm exec playwright test --reporter=list,html

## Container images
.PHONY: build-image
build-image:  ## Build Docker Image
	@DOCKER_BUILDKIT=1 docker build . -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile
