SHELL := /bin/bash

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install dependencies
	pnpm install

.PHONY: start
start: ## Start the Nick server
	pnpm start

.PHONY: migrate
migrate: ## Run database migrations
	pnpm migrate

.PHONY: seed
seed: ## Seed the database
	pnpm seed

.PHONY: lint
lint: ## Run lint checks
	pnpm lint
	pnpm prettier

.PHONY: test
test: ## Run tests
	pnpm test
