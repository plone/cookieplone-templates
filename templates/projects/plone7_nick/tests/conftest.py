"""Pytest configuration."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def cookieplone_root() -> dict:
    """Cookieplone root dir."""
    return Path().cwd().resolve().parent


@pytest.fixture(scope="session")
def context(cookieplone_root) -> dict:
    """Cookiecutter context."""
    return {
        "title": "Plone",
        "project_slug": "plone",
        "description": "A standalone Nick-based Plone project.",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "github_organization": "collective",
        "npm_package_name": "plone",
        "__cookieplone_repository_path": f"{cookieplone_root}",
    }


@pytest.fixture
def build_files_list():
    def func(root_dir: Path) -> list[Path]:
        """Build a list containing absolute paths to the generated files."""
        return [path for path in Path(root_dir).glob("*") if path.is_file()]

    return func


@pytest.fixture(scope="session")
def cutter_result(cookies_session, context):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context)
