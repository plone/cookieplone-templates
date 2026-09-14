"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "ci/gh_monorepo_addon"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "plone_version": "6.1.4",
            "python_version": "3.13",
            "python_package_name": "collective.addon",
            "npm_package_name": "@plone-collective/volto-addon",
            "node_version": "24",
            "has_docs": "0",
        },
        cookieplone_root,
        "ci_gh_monorepo_addon",
    )


@pytest.fixture(scope="session")
def context_with_docs(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "plone_version": "6.1.4",
            "python_version": "3.13",
            "python_package_name": "collective.addon",
            "npm_package_name": "@plone-collective/volto-addon",
            "node_version": "24",
            "has_docs": "1",
        },
        cookieplone_root,
        "ci_gh_monorepo_addon",
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
    return [
        ("backend", "path-backend"),
        ("frontend", "path-frontend"),
        ("repository", "path-root"),
    ]


@pytest.fixture
def guarded() -> bool:
    """Whether each check is guarded by a paths filter flag."""
    return True


@pytest.fixture
def expects_python_version() -> bool:
    """Whether the changelog workflow pins a Python version."""
    return True
