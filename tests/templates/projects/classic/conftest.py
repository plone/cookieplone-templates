"""Pytest configuration."""

from copy import deepcopy

import pytest

PLONE_VERSION = "6.1.1"


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "projects/classic"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
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
            "devops_storage": "relstorage",
        },
        cookieplone_root,
        "project",
    )


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
def context_no_docs(context) -> dict:
    """Cookiecutter context."""
    new_context = deepcopy(context)
    new_context["initialize_documentation"] = "0"
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
        "devops_storage": " ",  # error
    }


@pytest.fixture(scope="module")
def cutter_result_devops_no_ansible(
    template_path, cookies_module, context_devops_no_ansible
):
    """Cookiecutter result."""
    return cookies_module.bake(
        extra_context=context_devops_no_ansible, template=template_path
    )


@pytest.fixture(scope="module")
def cutter_result_devops_no_gha_deploy(
    template_path, cookies_module, context_devops_no_gha_deploy
):
    """Cookiecutter result."""
    return cookies_module.bake(
        extra_context=context_devops_no_gha_deploy, template=template_path
    )


@pytest.fixture(scope="module")
def cutter_result_no_docs(template_path, cookies_module, context_no_docs):
    """Cookiecutter result."""
    return cookies_module.bake(extra_context=context_no_docs, template=template_path)


@pytest.fixture(scope="module")
def cutter_devops_result_cache(template_path, cookies_module, context_devops_cache):
    """Cookiecutter result."""
    return cookies_module.bake(
        extra_context=context_devops_cache, template=template_path
    )


@pytest.fixture(scope="module")
def cutter_result_devops_no_cache(
    template_path, cookies_module, context_devops_no_cache
):
    """Cookiecutter result."""
    return cookies_module.bake(
        extra_context=context_devops_no_cache, template=template_path
    )
