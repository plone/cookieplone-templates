"""Pytest configuration."""

from copy import deepcopy
from pathlib import Path

import pytest

PLONE_VERSION = "6.1.0"


@pytest.fixture(scope="session")
def cookieplone_root() -> dict:
    """Cookieplone root dir."""
    parent = Path().cwd().resolve().parent
    return parent


@pytest.fixture(scope="session")
def context(cookieplone_root) -> dict:
    """Cookiecutter context."""
    return {
        "title": "Plone Brasil",
        "project_slug": "plone.org.br",
        "description": "Brazilian community website.",
        "hostname": "plone.org.br",
        "author": "PloneGov-BR",
        "email": "gov@plone.org.br",
        "use_prerelease_versions": "Yes",
        "plone_version": PLONE_VERSION,
        "python_package_name": "plonegov.ploneorgbr",
        "language_code": "en",
        "github_organization": "plonegovbr",
        "__project_git_initialize": "1",
        "container_registry": "github",
        "__cookieplone_repository_path": f"{cookieplone_root}",
    }


@pytest.fixture(scope="session")
def context_devops_cache(context) -> dict:
    """Cookiecutter context."""
    new_context = deepcopy(context)
    new_context["devops_cache"] = "1"
    return new_context


@pytest.fixture(scope="session")
def context_no_git(context) -> dict:
    """Cookiecutter context."""
    new_context = deepcopy(context)
    new_context["__project_git_initialize"] = "0"
    return new_context


@pytest.fixture(scope="session")
def context_devops_no_cache(context) -> dict:
    """Cookiecutter context."""
    new_context = deepcopy(context)
    new_context["devops_cache"] = "0"
    return new_context


@pytest.fixture(scope="session")
def context_devops_no_ansible(context) -> dict:
    """Cookiecutter context."""
    new_context = deepcopy(context)
    new_context["devops_ansible"] = "0"
    return new_context


@pytest.fixture(scope="session")
def context_devops_no_gha_deploy(context) -> dict:
    """Cookiecutter context."""
    new_context = deepcopy(context)
    new_context["devops_gha_deploy"] = "0"
    return new_context


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Plone Brasil",
        "project_slug": "plone.org.br",
        "description": "Brazilian community website.",
        "hostname": "https://plone.org.br",  # error
        "author": "PloneGov-BR",
        "email": "gov@plone.org.br",
        "python_package_name": "plone-org-br",  # error
        "plone_version": "5.2.8",  # error
        "language_code": "en-",  # error
        "github_organization": "plonegovbr",
        "container_registry": " ",  # error
    }


@pytest.fixture(scope="session")
def cutter_result(cookies_session, context):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context)


@pytest.fixture(scope="session")
def cutter_result_devops_no_ansible(cookies_session, context_devops_no_ansible):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context_devops_no_ansible)


@pytest.fixture(scope="session")
def cutter_result_devops_no_gha_deploy(cookies_session, context_devops_no_gha_deploy):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context_devops_no_gha_deploy)


@pytest.fixture(scope="session")
def cutter_devops_result_cache(cookies_session, context_devops_cache):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context_devops_cache)


@pytest.fixture(scope="session")
def cutter_result_devops_no_cache(cookies_session, context_devops_no_cache):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context_devops_no_cache)
