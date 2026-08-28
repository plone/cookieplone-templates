"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "sub/nick_backend"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Project Title",
            "project_slug": "project-title",
            "description": "Plone using Nick as backend.",
            "author": "Plone Community",
            "email": "collective@plone.org",
            "github_organization": "collective",
            "npm_package_name": "project-title",
            "nick_frontend": "volto",
        },
        cookieplone_root,
        "sub_nick_backend",
    )
