"""Pytest configuration for documentation_addon template tests."""

from pathlib import Path
from typing import Dict

import pytest

# List of expected files in the generated output
EXPECTED_FILES = [
    "CHANGES.md",
    "LICENSE",
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


@pytest.fixture(scope="session")
def template_dir() -> Path:
    """Path to the documentation_addon template directory."""
    return Path().cwd().resolve()


@pytest.fixture(scope="session")
def default_context() -> Dict[str, str]:
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
        "__documentation_addon_git_initialize": "1",
    }


@pytest.fixture(scope="session")
def no_git_context(default_context) -> Dict[str, str]:
    """Context with Git initialization disabled."""
    context = default_context.copy()
    context["__folder_name"] = "collective.docsnogit"
    context["__documentation_addon_git_initialize"] = "0"
    return context


@pytest.fixture
def bake_template(template_dir):
    """Fixture to bake the template with a given context."""

    def _bake(context: Dict[str, str], output_dir: Path) -> Path:
        from cookiecutter.main import cookiecutter

        cookiecutter(
            str(template_dir),
            no_input=True,
            extra_context=context,
            output_dir=str(output_dir),
        )
        return output_dir / context["__folder_name"]

    return _bake
