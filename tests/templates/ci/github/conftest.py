"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "ci/github"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Project Title",
            "folder_name": ".github",
            "organization": "collective",
            "project_slug": "project-title",
            "repository_url": "https://github.com/collective/project-title",
            "hostname": "project.example.com",
            "has_backend": "1",
            "has_docs": "1",
            "has_frontend": "1",
            "has_varnish": "1",
            "has_gha_deploy": "1",
        },
        cookieplone_root,
        "ci_github",
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
