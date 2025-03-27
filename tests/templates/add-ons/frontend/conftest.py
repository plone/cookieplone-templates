"""Pytest configuration."""

from copy import deepcopy

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "add-ons/frontend"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "frontend_addon_name": "volto-addon",
            "title": "Volto Add-on",
            "description": "Add new features to your Volto Project.",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "github_organization": "collective",
            "npm_package_name": "@plone-collective/volto-addon",
            "volto_version": "18.10.0",
        },
        cookieplone_root,
        "frontend_addon",
    )


@pytest.fixture(scope="session")
def context_no_npm_organization(context) -> dict:
    """Cookiecutter context without a NPM organization."""
    new_context = deepcopy(context)
    new_context["npm_package_name"] = "volto-addon"
    return new_context


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "frontend_addon_name": "volto addon",
        "title": "Volto Add-on",
        "description": "Add new features to your Volto Project.",
        "github_organization": "collective",
        "npm_package_name": "plone-collective/volto-addon",
        "author": "Plone Collective",
        "email": "collective@plone.org",
    }
