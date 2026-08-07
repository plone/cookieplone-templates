"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "projects/aurora_nick"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Plone",
            "project_slug": "plone",
            "description": "Plone Aurora using Nick as backend.",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "github_organization": "collective",
            "npm_package_name": "plone",
            "frontend_addon_name": "aurora-plone",
        },
        cookieplone_root,
        "aurora_nick",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Plone",
        "project_slug": "plone",
        "description": "Plone Aurora using Nick as backend.",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "github_organization": "collective",
        "npm_package_name": "plone collective",
        "frontend_addon_name": "aurora-plone",
    }
