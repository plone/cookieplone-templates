"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "projects/plone7_nick_bff"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Volto Add-on",
            "frontend_addon_name": "volto-addon",
            "project_slug": "volto-addon",
            "description": "Add new features to your Volto Project.",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "github_organization": "collective",
            "npm_package_name": "@plone-collective/volto-addon",
            "volto_version": "18.10.0",
        },
        cookieplone_root,
        "plone7_nick_bff",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Volto Add-on",
        "frontend_addon_name": "volto addon",
        "project_slug": "volto-addon",
        "description": "Add new features to your Volto Project.",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "github_organization": "collective",
        "npm_package_name": "plone-collective/volto-addon",
        "volto_version": "18.10.0",
    }
