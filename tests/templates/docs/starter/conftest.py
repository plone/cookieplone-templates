"""Pytest configuration for documentation_starter template tests."""

from copy import deepcopy

import pytest

# List of expected files in the generated output
EXPECTED_FILES = [
    ".gitignore",
    ".vale.ini",
    "LICENSE.md",
    "Makefile",
    "pyproject.toml",
    "README.md",
    "docs/_static/favicon.ico",
    "docs/_static/logo.svg",
    "docs/_templates/404.html",
    "docs/concepts/index.md",
    "docs/how-to-guides/index.md",
    "docs/reference/index.md",
    "docs/tutorials/index.md",
    "docs/.readthedocs.yaml",
    "docs/conf.py",
    "docs/glossary.md",
    "docs/index.md",
    "docs/robots.txt",
    "styles/config/vocabularies/Plone/accept.txt",
    "styles/config/vocabularies/Plone/reject.txt",
    "styles/config/vocabularies/Base/accept.txt",
    "styles/config/vocabularies/Base/reject.txt",
]


@pytest.fixture(scope="module")
def template_folder() -> str:
    """Path to the documentation_starter template directory."""
    return "docs/starter"


@pytest.fixture(scope="session")
def context() -> dict[str, str]:
    """Default context for baking the template."""
    return {
        "title": "My Documentation",
        "project_description": "Documentation for a Plone project",
        "author_name": "Plone Community",
        "author_email": "collective@plone.org",
        "github_organization": "collective",
        "__folder_name": "collective.docs",
        "__normalized_package_name": "collective.docs",
        "repository_url": "https://github.com/collective/collective.docs",
        "version": "1.0.0",
        "min_python_version": "3.8",
        "initialize_git": "1",
    }


@pytest.fixture(scope="session")
def no_git_context(default_context) -> dict[str, str]:
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
    if "root_file_path" in metafunc.fixturenames:
        metafunc.parametrize("root_file_path", EXPECTED_FILES)
