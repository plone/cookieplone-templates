"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "sub/frontend_project"


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
