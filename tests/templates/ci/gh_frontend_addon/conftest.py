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


@pytest.fixture
def codebases() -> list[tuple[str, str]]:
    """Codebases checked by this template, and the config output holding each path."""
    return [("frontend", "path-frontend")]


@pytest.fixture
def guarded() -> bool:
    """Whether each check is guarded by a paths filter flag."""
    return False


@pytest.fixture
def expects_python_version() -> bool:
    """Whether the changelog workflow pins a Python version."""
    return False
