"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "projects/aurora_nick_embedded"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Plone Aurora (alpha) using Nick as an embedded library (experimental)",
            "frontend_addon_name": "aurora-nick-embedded",
            "project_slug": "aurora-nick-embedded",
            "description": "Plone Aurora using Nick as an embedded library.",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "github_organization": "collective",
            "npm_package_name": "@plone-collective/aurora-nick-embedded",
        },
        cookieplone_root,
        "aurora_nick_embedded",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Plone Aurora (alpha) using Nick as an embedded library (experimental)",
        "frontend_addon_name": "aurora-nick-embedded",
        "project_slug": "aurora-nick-embedded",
        "description": "Plone Aurora using Nick as an embedded library.",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "github_organization": "collective",
        "npm_package_name": "plone-collective/aurora-nick-embedded",
    }
