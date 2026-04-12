"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "add-ons/seven_addon"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "frontend_addon_name": "seven-addon",
            "title": "Seven Add-on",
            "description": "A new add-on for Seven.",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "github_organization": "collective",
            "npm_package_name": "@plone-collective/seven-addon",
            "volto_version": "18.10.0",
        },
        cookieplone_root,
        "seven_addon",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "frontend_addon_name": "seven addon",
        "title": "Seven Add-on",
        "description": "A new add-on for Seven.",
        "github_organization": "collective",
        "npm_package_name": "plone-collective/seven-addon",
        "author": "Plone Collective",
        "email": "collective@plone.org",
    }
