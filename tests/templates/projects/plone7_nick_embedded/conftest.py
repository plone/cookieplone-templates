"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "projects/plone7_nick_embedded"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Plone 7 alpha using Nick as an embedded library (experimental)",
            "frontend_addon_name": "plone7-nick-embedded",
            "project_slug": "plone7-nick-embedded",
            "description": "Add new features to your Plone 7 Project.",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "github_organization": "collective",
            "npm_package_name": "@plone-collective/plone7-nick-embedded",
        },
        cookieplone_root,
        "plone7_nick_embedded",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Plone 7 alpha using Nick as an embedded library (experimental)",
        "frontend_addon_name": "plone7-nick-embedded",
        "project_slug": "plone7-nick-embedded",
        "description": "Add new features to your Plone 7 Project.",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "github_organization": "collective",
        "npm_package_name": "plone-collective/plone7-nick-embedded",
    }
