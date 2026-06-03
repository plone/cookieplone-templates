"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "ci/gh_project"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "hostname": "example.com",
            "python_version": "3.13",
            "python_package_name": "collective.addon",
            "npm_package_name": "@plone-collective/volto-addon",
            "node_version": "24",
            "has_docs": "0",
            "has_cache": "0",
            "has_deploy": "0",
        },
        cookieplone_root,
        "ci_gh_project",
    )


@pytest.fixture(scope="session")
def context_with_docs(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "hostname": "example.com",
            "python_version": "3.13",
            "python_package_name": "collective.addon",
            "npm_package_name": "@plone-collective/volto-addon",
            "node_version": "24",
            "has_docs": "1",
            "has_cache": "0",
            "has_deploy": "0",
        },
        cookieplone_root,
        "ci_gh_project",
    )


@pytest.fixture(scope="session")
def context_with_cache(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "hostname": "example.com",
            "python_version": "3.13",
            "python_package_name": "collective.addon",
            "npm_package_name": "@plone-collective/volto-addon",
            "node_version": "24",
            "has_docs": "0",
            "has_cache": "1",
            "has_deploy": "0",
        },
        cookieplone_root,
        "ci_gh_project",
    )


@pytest.fixture(scope="session")
def context_with_deploy(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "hostname": "example.com",
            "python_version": "3.13",
            "python_package_name": "collective.addon",
            "npm_package_name": "@plone-collective/volto-addon",
            "node_version": "24",
            "has_docs": "0",
            "has_cache": "0",
            "has_deploy": "1",
        },
        cookieplone_root,
        "ci_gh_project",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "npm_package_name": "",
        "node_version": "24.x",
    }
