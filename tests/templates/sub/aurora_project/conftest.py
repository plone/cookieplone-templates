"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "sub/aurora_project"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Aurora project",
            "author": "Plone Collective",
            "aurora_version": "1.0.0-alpha.19",
            "__cookieplone_repository_path": f"{cookieplone_root}",
        },
        cookieplone_root,
        "aurora_project",
    )
