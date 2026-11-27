SHELL := /bin/bash

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: backend-install frontend-install ## Install backend and frontend dependencies

.PHONY: backend-install
backend-install: ## Install the Nick backend
	$(MAKE) -C backend install

.PHONY: backend-start
backend-start: ## Start the Nick backend
	$(MAKE) -C backend start

.PHONY: backend-migrate
backend-migrate: ## Run Nick database migrations and install the profiles
	$(MAKE) -C backend migrate

.PHONY: backend-build-image
backend-build-image: ## Build the Nick backend image, on the official plone/nick image
	$(MAKE) -C backend build-image

.PHONY: backend-test
backend-test: ## Test the Nick backend
	$(MAKE) -C backend test

.PHONY: frontend-install
frontend-install: ## Install the Volto frontend
	$(MAKE) -C frontend install

.PHONY: frontend-start
frontend-start: ## Start the Volto frontend
	$(MAKE) -C frontend start

.PHONY: frontend-build
frontend-build: ## Build the Volto frontend
	$(MAKE) -C frontend build

.PHONY: frontend-test
frontend-test: ## Test the Volto frontend
	$(MAKE) -C frontend test

.PHONY: lint
lint: ## Lint backend and frontend
	$(MAKE) -C backend lint
	$(MAKE) -C frontend lint

.PHONY: test
test: backend-test frontend-test ## Test backend and frontend
