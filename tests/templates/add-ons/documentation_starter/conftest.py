"""Pytest configuration for documentation_starter template tests."""

from copy import deepcopy
from typing import Dict

import pytest

# List of expected files in the generated output
EXPECTED_FILES = [
    "LICENSE.GPL",
    "LICENSE.md",
    "Makefile",
    "pyproject.toml",
    "README.md",
    "docs/conf.py",
    "docs/glossary.md",
    "docs/guides/getting-started.md",
    "docs/guides/usage.md",
    "docs/index.md",
    "docs/reference/file-system-structure.md",
    "docs/reference/theme-elements.md",
    "docs/robots.txt",
    "docs/_static/favicon.ico",
    "docs/_static/logo.svg",
]


@pytest.fixture(scope="module")
def template_folder() -> str:
    """Path to the documentation_starter template directory."""
    return "add-ons/documentation_starter"


@pytest.fixture(scope="session")
def context() -> Dict[str, str]:
    """Default context for baking the template."""
    return {
        "title": "My Documentation",
        "project_description": "Documentation for a Plone project",
        "author_name": "Plone Community",
        "author_email": "collective@plone.org",
        "github_organization": "collective",
        "__folder_name": "collective.docs",
        "repository_url": "https://github.com/collective/collective.docs",
        "version": "1.0.0",
        "min_python_version": "3.8",
        "initialize_git": "1",
    }


@pytest.fixture(scope="session")
def no_git_context(default_context) -> Dict[str, str]:
    """Context with Git initialization disabled."""
    context = deepcopy(default_context)
    context["__folder_name"] = "collective.docsnogit"
    context["initialize_git"] = "0"
    return context


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Addon",
        "description": "A Tech blog.",
        "github_organization": "collective",
        "python_package_name": "collective_addon",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "feature_headless": "1",
    }


def pytest_generate_tests(metafunc):
    print("Here it is====================================")
    if "root_file_path" in metafunc.fixturenames:
        metafunc.parametrize("root_file_path", EXPECTED_FILES)
