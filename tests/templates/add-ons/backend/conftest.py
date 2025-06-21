"""Pytest configuration."""

from copy import deepcopy

import pytest

ROOT_FILES = [
    ".editorconfig",
    ".github/workflows/ci.yml",
    ".gitignore",
    "CHANGELOG.md",
    "CONTRIBUTORS.md",
    "instance.yaml",
    "LICENSE.GPL",
    "LICENSE.md",
    "Makefile",
    "mx.ini",
    "pyproject.toml",
    "README.md",
    "scripts/create_site.py",
]


PKG_SRC_FILES = [
    "__init__.py",
    "configure.zcml",
    "content/__init__.py",
    "controlpanel/__init__.py",
    "controlpanel/configure.zcml",
    "dependencies.zcml",
    "indexers/__init__.py",
    "indexers/configure.zcml",
    "locales/__init__.py",
    "locales/__main__.py",
    "profiles/default/browserlayer.xml",
    "profiles/default/catalog.xml",
    "profiles/default/controlpanel.xml",
    "profiles/default/diff_tool.xml",
    "profiles/default/metadata.xml",
    "profiles/default/repositorytool.xml",
    "profiles/default/rolemap.xml",
    "profiles/default/types.xml",
    "profiles/default/types/.gitkeep",
    "profiles/uninstall/browserlayer.xml",
    "setuphandlers/__init__.py",
    "testing.py",
    "upgrades/__init__.py",
    "upgrades/configure.zcml",
    "vocabularies/__init__.py",
    "vocabularies/configure.zcml",
]


PKG_SRC_FEATURE_HEADLESS = [
    "serializers/__init__.py",
    "serializers/configure.zcml",
]


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "add-ons/backend"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "title": "Addon",
            "description": "A Tech blog.",
            "github_organization": "collective",
            "python_package_name": "collective.addon",
            "author": "Plone Collective",
            "email": "collective@plone.org",
            "feature_headless": "1",
            "__backend_addon_git_initialize": "1",
        },
        cookieplone_root,
        "backend_addon",
    )


@pytest.fixture(scope="session")
def context_no_headless(context) -> dict:
    """Cookiecutter context without headless feature enabled."""
    new_context = deepcopy(context)
    new_context["python_package_name"] = "collective.addonredux"
    new_context["feature_headless"] = "0"
    return new_context


@pytest.fixture(scope="session")
def context_distribution(context) -> dict:
    """Cookiecutter context with distribution enabled."""
    new_context = deepcopy(context)
    new_context["python_package_name"] = "plonedistribution.myplone"
    new_context["__feature_distribution"] = "1"
    return new_context


@pytest.fixture(scope="session")
def context_no_git(context) -> dict:
    """Cookiecutter context without Git repository."""
    new_context = deepcopy(context)
    new_context["python_package_name"] = "collective.addonnogit"
    new_context["__backend_addon_git_initialize"] = "0"
    return new_context


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {
        "title": "Addon",
        "description": "A Tech blog.",
        "github_organization": "collective",
        "python_package_name": "collective_addon",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "feature_headless": "1",
    }


@pytest.fixture(scope="module")
def cutter_result_no_namespace(context, template_path, cookies_module) -> dict:
    """Cookiecutter context without namespace package."""
    new_context = deepcopy(context)
    new_context["python_package_name"] = "addon"
    return cookies_module.bake(extra_context=new_context, template=template_path)


@pytest.fixture(scope="module")
def cutter_result_two_namespaces(context, template_path, cookies_module) -> dict:
    """Cookiecutter context with 2 namespace packages."""
    new_context = deepcopy(context)
    new_context["python_package_name"] = "foo.bar.baz"
    return cookies_module.bake(extra_context=new_context, template=template_path)


def pytest_generate_tests(metafunc):
    if "root_file_path" in metafunc.fixturenames:
        metafunc.parametrize("root_file_path", ROOT_FILES)
    if "pkg_file_path" in metafunc.fixturenames:
        metafunc.parametrize("pkg_file_path", PKG_SRC_FILES)
    if "pkg_file_path_headless" in metafunc.fixturenames:
        metafunc.parametrize("pkg_file_path_headless", PKG_SRC_FEATURE_HEADLESS)
