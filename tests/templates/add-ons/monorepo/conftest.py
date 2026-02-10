"""Pytest configuration."""

from copy import deepcopy

import pytest

PLONE_VERSION = "6.1.14"
VOLTO_VERSION = "18.10.0"


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "add-ons/monorepo"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Volto Add-on",
            "description": "Add new features to your Volto Project.",
            "project_slug": "collective-addon",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "github_organization": "collective",
            "hostname": "plone.org.br",
            "use_prerelease_versions": "Yes",
            "plone_version": PLONE_VERSION,
            "volto_version": VOLTO_VERSION,
            "python_package_name": "collective.addon",
            "npm_package_name": "@plone-collective/volto-addon",
            "container_registry": "github",
        },
        cookieplone_root,
        "monorepo_addon",
    )


@pytest.fixture(scope="session")
def context_no_npm_organization(context) -> dict:
    """Cookiecutter context without a NPM organization."""
    new_context = deepcopy(context)
    new_context["npm_package_name"] = "volto-addon"
    return new_context


@pytest.fixture(scope="module")
def cutter_result_no_organization(
    template_path, cookies_module, context_no_npm_organization
):
    """Cookiecutter result."""
    return cookies_module.bake(
        extra_context=context_no_npm_organization, template=template_path
    )
