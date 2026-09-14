SHELL := /bin/bash
CURRENT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BASE_FOLDER := $(shell git rev-parse --show-toplevel)
FOLDER_NAME := $(shell basename $(CURRENT_DIR))
TEMPLATE := ci_$(FOLDER_NAME)
PROJECT_FOLDER_NAME := .github

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: generate
generate: ## Generate a sample configuration
	rm -rf $(PROJECT_FOLDER_NAME)
	COOKIEPLONE_REPOSITORY=$(BASE_FOLDER) uv run cookieplone $(TEMPLATE) --no-input

.PHONY: test
test: ## Test the template
	uv run pytest $(BASE_FOLDER)/tests/templates/ci/$(FOLDER_NAME)
