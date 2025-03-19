# Makefile for Sphinx documentation
.DEFAULT_GOAL   = help
SHELL           = bash

# You can set these variables from the command line.
SPHINXOPTS      ?=
PAPER           ?=

# Internal variables.
GREEN=`tput setaf 2`
RESET=`tput sgr0`
SPHINXBUILD     = "$(realpath .venv/bin/sphinx-build)"
SPHINXAUTOBUILD = "$(realpath .venv/bin/sphinx-autobuild)"
DOCS_DIR        = ./docs/
BUILDDIR        = ../_build
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help:  # This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# environment management
.venv/bin/python:  ## Create Python virtual environment and install package requirements
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip setuptools uv wheel
	.venv/bin/uv pip install -r requirements.txt

.PHONY: docs
docs: .venv/bin/python  ## Install documentation requirements into Python virtual environment
	.venv/bin/uv pip install -r requirements-docs.txt -e .

.PHONY: dev
dev: docs  ## Install development requirements into Python virtual environment

	.venv/bin/uv pip install -r requirements-dev.txt -e .

.PHONY: update-deps
update-deps:  ## Update
	.venv/bin/python  ## Install documentation requirements into Python virtual environment
	.venv/bin/uv pip install --upgrade pip setuptools uv wheel
	.venv/bin/uv pip compile --upgrade pyproject.toml -o requirements.txt
	.venv/bin/uv pip compile --upgrade pyproject.toml \
		--extra docs -o requirements-docs.txt
	.venv/bin/uv pip compile --upgrade pyproject.toml \
		--extra docs --extra dev -o requirements-dev.txt

.PHONY: clean
clean:  ## Clean docs build directory
	cd $(DOCS_DIR) && rm -rf $(BUILDDIR)/

.PHONY: clean-python
clean-python: clean
	rm -rf .venv/
# /environment management

# documentation builders
.PHONY: html
html: .venv/bin/python  ## Build html
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

.PHONY: livehtml
livehtml: docs  ## Rebuild Sphinx documentation on changes, with live-reload in the browser
	cd "$(DOCS_DIR)" && ${SPHINXAUTOBUILD} \
		--ignore "*.swp" \
		--port 8050 \
		-b html . "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

.PHONY: dirhtml
dirhtml: docs
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

.PHONY: singlehtml
singlehtml: docs
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

.PHONY: text
text: docs
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

.PHONY: changes
changes: docs
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."
# /documentation builders

# test
.PHONY: linkcheck
linkcheck: docs  ## Run linkcheck
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
		"or in $(BUILDDIR)/linkcheck/ ."

.PHONY: linkcheckbroken
linkcheckbroken: docs  ## Run linkcheck and show only broken links
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck | GREP_COLORS='0;31' grep -wi "broken\|redirect" --color=always | GREP_COLORS='0;31' grep -vi "https://github.com/plone/volto/issues/" --color=always && if test $$? = 0; then exit 1; fi || test $$? = 1
	@echo
	@echo "Link check complete; look for any errors in the above output " \
		"or in $(BUILDDIR)/linkcheck/ ."

.PHONY: doctest
doctest: docs  ## Test snippets in the documentation
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."

.PHONY: pytest
test: .venv/bin/python
	@echo "$(GREEN)==> Test template$(RESET)"
	.venv/bin/uv run pytest tests

.PHONY: test
test: clean pytest linkcheckbroken doctest  ## Clean docs build, then run linkcheckbroken
# development

.PHONY: all
all: clean linkcheck html  ## Clean docs build, then run linkcheck, and build html
# /development
