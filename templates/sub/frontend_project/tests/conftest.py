"""Pytest configuration."""

from pathlib import Path
from typing import List

import pytest


@pytest.fixture(scope="session")
def cookieplone_root() -> dict:
    """Cookieplone root dir."""
    parent = Path().cwd().resolve().parent
    return parent


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Frontend project",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "volto_version": "18.10.0",
            "__cookieplone_repository_path": f"{cookieplone_root}",
        },
        cookieplone_root,
        "frontend_project",
    )


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
