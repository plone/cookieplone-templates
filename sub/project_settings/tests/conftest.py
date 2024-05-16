"""Pytest configuration."""

import re
from copy import deepcopy
from pathlib import Path
from typing import List

import pytest


@pytest.fixture(scope="session")
def variable_pattern():
    return re.compile("{{( ?cookiecutter)[.](.*?)}}")


@pytest.fixture(scope="session")
def cookieplone_root() -> dict:
    """Cookieplone root dir."""
    parent = Path().cwd().resolve().parent
    return parent


@pytest.fixture(scope="session")
def context(cookieplone_root) -> dict:
    """Cookiecutter context."""
    return {
        "title": "Project Title",
        "description": "A new project using Plone 6.",
        "project_slug": "project-title",
        "author": "Plone Foundation",
        "email": "collective@plone.org",
        "python_package_name": "project.title",
        "frontend_addon_name": "volto-project-title",
        "language_code": "en",
        "github_organization": "collective",
        "__node_version": "20",
        "__cookieplone_repository_path": f"{cookieplone_root}",
    }


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Frontend project",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "volto_version": "---",
    }


@pytest.fixture
def build_files_list():
    def func(root_dir: Path) -> List[Path]:
        """Build a list containing absolute paths to the generated files."""
        return [path for path in Path(root_dir).glob("*") if path.is_file()]

    return func


@pytest.fixture(scope="session")
def cutter_result(cookies_session, context):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context)
