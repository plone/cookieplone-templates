SHELL := /bin/bash

IMAGE_NAME ?= {{ cookiecutter.project_slug }}-backend
IMAGE_TAG ?= latest

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install dependencies
	mkdir -p src
	pnpm dlx mrs-developer missdev --config=tsconfig.json --fetch-https
	pnpm install

.PHONY: start
start: ## Start the Nick server
	pnpm start

.PHONY: migrate
migrate: ## Run the database migrations and install the profiles
	pnpm migrate

.PHONY: lint
lint: ## Run lint checks
	pnpm lint
	pnpm prettier

.PHONY: test
test: ## Run tests
	pnpm test

.PHONY: build-image
build-image: ## Build the production image, on the official plone/nick image
	docker build . -t $(IMAGE_NAME):$(IMAGE_TAG)
