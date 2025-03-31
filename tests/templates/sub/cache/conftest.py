"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "sub/cache"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Project Title",
            "description": "A new project using Plone 6.",
            "project_slug": "project-title",
            "hostname": "project.example.com",
            "author": "Plone Foundation",
            "email": "collective@plone.org",
            "python_package_name": "project.title",
            "github_organization": "collective",
        },
        cookieplone_root,
        "sub_cache",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": " ",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "volto_version": "---",
    }
