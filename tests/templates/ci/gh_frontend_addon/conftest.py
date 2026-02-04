"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "ci/gh_frontend_addon"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "npm_package_name": "volto-addon",
            "node_version": "24.x",
        },
        cookieplone_root,
        "ci_gh_frontend_addon",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "npm_package_name": "",
        "node_version": "24.x",
    }
