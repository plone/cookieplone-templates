"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "sub/addon_settings"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Collective Add-on",
            "description": "A new add-on for Plone.",
            "project_slug": "collective-addon",
            "author": "Plone Foundation",
            "email": "collective@plone.org",
            "python_package_name": "collective.addon",
            "npm_package_name": "@plone-collective/volto-collective-addon",
            "github_organization": "collective",
            "use_prerelease_versions": "No",
        },
        cookieplone_root,
        "project_settings",
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
