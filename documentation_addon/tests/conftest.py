"""Pytest configuration for documentation_addon."""

from copy import deepcopy
from pathlib import Path
from typing import List

import pytest

# Expected root files for documentation_addon
ROOT_FILES = [
    "CHANGES.md",
    "LICENSE",
    "Makefile",
    "MANIFEST.in",
    "pyproject.toml",
    "README.md",
    # Note: requirements-*.txt should be removed in favor of pyproject.toml, but kept here if still present
    "requirements-dev.txt",
    "requirements-docs.txt",
    "requirements.txt",
]

# Expected docs files (relative to docs/)
DOCS_FILES = [
    "conf.py",
    "glossary.md",
    "guides/getting-started.md",
    "guides/usage.md",
    "index.md",
    "reference/file-system-structure.md",
    "reference/index.md",
    "reference/theme-elements.md",
    "robots.txt",
    "_static/favicon.ico",
    "_static/logo.svg",
]


@pytest.fixture(scope="session")
def cookieplone_root() -> Path:
    """Cookieplone root dir."""
    return Path().cwd().resolve().parent


@pytest.fixture(scope="session")
def context(cookieplone_root) -> dict:
    """Cookiecutter context for documentation_addon."""
    return {
        "title": "My Documentation",
        "project_description": "Documentation for a Plone project.",
        "author_name": "Plone Community",
        "author_email": "collective@plone.org",
        "github_organization": "collective",
        "__folder_name": "collective.docs",
        "repository_url": "https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.__folder_name }}",
        "version": "1.0.0",
        "min_python_version": "3.8",
        "__cookieplone_repository_path": str(cookieplone_root),
    }


@pytest.fixture(scope="session")
def context_no_git(context) -> dict:
    """Cookiecutter context without Git repository initialization."""
    new_context = deepcopy(context)
    new_context["__folder_name"] = "collective.docsnogit"
    new_context["__documentation_addon_git_initialize"] = "0"  # Optional, if you add this toggle
    return new_context


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Invalid Docs",
        "project_description": "Broken config.",
        "author_name": "Unknown",
        "author_email": "invalid@email",  # Missing domain
        "github_organization": "collective",
        "__folder_name": "collective_docs_invalid",  # Invalid naming
    }


@pytest.fixture
def build_files_list():
    """Build a list containing absolute paths to the generated files."""
    def func(root_dir: Path) -> List[Path]:
        return [path for path in root_dir.glob("**/*") if path.is_file()]
    return func


@pytest.fixture(scope="session")
def cutter_result(cookies_session, context):
    """Cookiecutter result for documentation_addon."""
    return cookies_session.bake(extra_context=context)


@pytest.fixture(scope="session")
def cutter_result_no_git(cookies_session, context_no_git):
    """Cookiecutter result without Git initialization."""
    return cookies_session.bake(extra_context=context_no_git)
