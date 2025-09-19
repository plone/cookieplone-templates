"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "sub/project_settings"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Project Title",
            "description": "A new project using Plone 6.",
            "project_slug": "project-title",
            "author": "Plone Foundation",
            "email": "collective@plone.org",
            "python_package_name": "project.title",
            "frontend_addon_name": "volto-project-title",
            "language_code": "en",
            "github_organization": "collective",
            "use_prerelease_versions": "No",
            "__node_version": "20",
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
