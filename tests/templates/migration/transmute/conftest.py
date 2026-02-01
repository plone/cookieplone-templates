"""Pytest configuration for migration_transmute template tests."""

from copy import deepcopy

import pytest

# List of expected files in the generated output
EXPECTED_FILES = [
    ".env_dist",
    ".gitignore",
    ".vscode/extensions.json",
    ".vscode/settings.json",
    "LICENSE.GPL",
    "LICENSE.md",
    "Makefile",
    "pyproject.toml",
    "README.md",
    "data/.gitkeep",
    "logs/.gitkeep",
    "reports/.gitkeep",
    "scripts/reports_as_csv.py",
    "src/plone_migration/__init__.py",
    "src/plone_migration/prepare/__init__.py",
    "src/plone_migration/processors/__init__.py",
    "src/plone_migration/steps/__init__.py",
    "src/plone_migration/utils/__init__.py",
    "transmute.toml",
]

EXPECTED_FOLDERS = [
    ".git",
    ".vscode",
    "data",
    "logs",
    "reports",
    "scripts",
    "src",
]


@pytest.fixture(scope="module")
def template_folder() -> str:
    """Path to the documentation_starter template directory."""
    return "migration/transmute"


@pytest.fixture(scope="session")
def context() -> dict[str, str]:
    """Default context for baking the template."""
    return {
        "title": "Plone Migration",
        "project_description": "Plone migration ETL using collective.transmute",
        "python_package_name": "plone_migration",
        "src_site_id": "Intranet",
        "dst_site_id": "Plone",
        "author_name": "Plone Community",
        "author_email": "collective@plone.org",
        "initialize_git": "1",
    }


@pytest.fixture(scope="session")
def no_git_context(default_context) -> dict[str, str]:
    """Context with Git initialization disabled."""
    context = deepcopy(default_context)
    context["initialize_git"] = "0"
    return context


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Plone Migration",
        "project_description": "Plone migration ETL using collective.transmute",
        "python_package_name": "plone migration",
        "src_site_id": "Intranet",
        "dst_site_id": "Plone",
        "author_name": "Plone Community",
        "author_email": "collective@plone.org",
        "initialize_git": "1",
    }


def pytest_generate_tests(metafunc):
    if "root_file_path" in metafunc.fixturenames:
        metafunc.parametrize("root_file_path", EXPECTED_FILES)
    if "root_folder_path" in metafunc.fixturenames:
        metafunc.parametrize("root_folder_path", EXPECTED_FOLDERS)
