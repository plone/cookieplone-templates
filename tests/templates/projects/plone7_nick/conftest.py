"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "projects/plone7_nick"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Plone",
            "project_slug": "plone",
            "description": "A standalone Nick-based Plone project.",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "github_organization": "collective",
            "npm_package_name": "plone",
        },
        cookieplone_root,
        "plone7_nick",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Plone",
        "project_slug": "plone",
        "description": "A standalone Nick-based Plone project.",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "github_organization": "collective",
        "npm_package_name": "plone collective",
    }
