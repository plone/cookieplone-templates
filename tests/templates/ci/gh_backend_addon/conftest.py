"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "ci/gh_backend_addon"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "plone_version": "6.1.4",
            "python_version": "3.13",
        },
        cookieplone_root,
        "ci_gh_backend_addon",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "plone_version": "",
        "python_version": "",
    }
