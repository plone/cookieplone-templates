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

PLONE_VERSION=6
DOCKER_IMAGE=plone/server-dev:${PLONE_VERSION}
DOCKER_IMAGE_ACCEPTANCE=plone/server-acceptance:${PLONE_VERSION}

.PHONY: help
help: ## Show this help
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

# Dev Helpers

.PHONY: install
install: ## Installs the project in a development environment
	@echo "$(GREEN)Install$(RESET)"
	pnpm dlx mrs-developer missdev --no-config --fetch-https
	pnpm i
	make build-deps

.PHONY: start
start: ## Starts Aurora in development mode
	pnpm start

.PHONY: build
build: ## Build a production bundle of the project
	pnpm build

core/packages/registry/dist: $(shell find core/packages/registry/src -type f)
	pnpm --filter @plone/registry build

core/packages/icons/dist: $(shell find core/packages/icons/src -type f)
	pnpm --filter @plone/icons build

core/packages/quanta/dist: $(shell find core/packages/quanta/src -type f)
	pnpm --filter @plone/quanta build

core/packages/components/dist: $(shell find core/packages/components/src -type f)
	pnpm --filter @plone/components build

core/packages/client/dist: $(shell find core/packages/client/src -type f)
	pnpm --filter @plone/client build

core/packages/helpers/dist: $(shell find core/packages/helpers/src -type f)
	pnpm --filter @plone/helpers build

core/packages/react-router/dist: $(shell find core/packages/react-router/src -type f)
	pnpm --filter @plone/react-router build

.PHONY: build-deps
build-deps: core/packages/registry/dist core/packages/icons/dist core/packages/quanta/dist core/packages/components/dist core/packages/client/dist core/packages/react-router/dist core/packages/helpers/dist ## Build dependencies

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

.PHONY: backend-docker-start
backend-docker-start:	## Starts a Docker-based backend for development
	@echo "$(GREEN)==> Start Docker-based Plone Backend$(RESET)"
	docker run -it --rm --name=backend -p 8080:8080 -e SITE=Plone $(DOCKER_IMAGE)

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
