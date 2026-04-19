"""Pytest configuration."""

from copy import deepcopy
from pathlib import Path
from typing import List

import pytest


@pytest.fixture(scope="session")
def cookieplone_root() -> dict:
    """Cookieplone root dir."""
    parent = Path().cwd().resolve().parent
    return parent


@pytest.fixture(scope="session")
def context(cookieplone_root) -> dict:
    """Cookiecutter context."""
    return {
        "frontend_addon_name": "plone7-nick-embedded",
        "title": "Plone 7 alpha using Nick as an embedded library",
        "project_slug": "plone7-nick-embedded",
        "description": "Add new features to your Plone 7 Project.",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "github_organization": "collective",
        "npm_package_name": "@plone-collective/plone7-nick-embedded",
        "__cookieplone_repository_path": f"{cookieplone_root}",
    }


@pytest.fixture(scope="session")
def context_no_npm_organization(context) -> dict:
    """Cookiecutter context without a NPM organization."""
    new_context = deepcopy(context)
    new_context["npm_package_name"] = "plone7-nick-embedded"
    return new_context


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "frontend_addon_name": "plone7 nick embedded",
        "title": "Plone 7 alpha using Nick as an embedded library",
        "project_slug": "plone7-nick-embedded",
        "description": "Add new features to your Plone 7 Project.",
        "github_organization": "collective",
        "npm_package_name": "plone-collective/plone7-nick-embedded",
        "author": "Plone Collective",
        "email": "collective@plone.org",
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
