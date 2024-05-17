"""Pytest configuration."""

import re
from copy import deepcopy
from pathlib import Path
from typing import List

import pytest

ROOT_FILES = [
    ".editorconfig",
    ".github/workflows/meta.yml",
    ".gitignore",
    ".meta.toml",
    ".pre-commit-config.yaml",
    "CHANGES.md",
    "constraints.txt",
    "CONTRIBUTORS.md",
    "instance.yaml",
    "LICENSE.GPL",
    "LICENSE.md",
    "Makefile",
    "MANIFEST.in",
    "mx.ini",
    "pyproject.toml",
    "README.md",
    "requirements.txt",
    "scripts/create_site.py",
    "setup.py",
    "tox.ini",
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
    "profiles/default/browserlayer.xml",
    "profiles/default/catalog.xml",
    "profiles/default/controlpanel.xml",
    "profiles/default/diff_tool.xml",
    "profiles/default/metadata.xml",
    "profiles/default/repositorytool.xml",
    "profiles/default/rolemap.xml",
    "profiles/default/theme.xml",
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


@pytest.fixture(scope="session")
def cookieplone_root() -> dict:
    """Cookieplone root dir."""
    parent = Path().cwd().resolve().parent
    return parent


@pytest.fixture(scope="session")
def variable_pattern():
    return re.compile("{{( ?cookiecutter)[.](.*?)}}")


@pytest.fixture(scope="session")
def context(cookieplone_root) -> dict:
    """Cookiecutter context."""
    return {
        "title": "Addon",
        "description": "A Tech blog.",
        "github_organization": "collective",
        "python_package_name": "collective.addon",
        "author": "Plone Collective",
        "email": "collective@plone.org",
        "feature_headless": "1",
        "__backend_addon_git_initialize": "1",
        "__cookieplone_repository_path": f"{cookieplone_root}",
    }


@pytest.fixture(scope="session")
def context_no_headless(context) -> dict:
    """Cookiecutter context without headless feature enabled."""
    new_context = deepcopy(context)
    new_context["python_package_name"] = "collective.addonredux"
    new_context["feature_headless"] = "0"
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


@pytest.fixture
def build_files_list():
    def func(root_dir: Path) -> List[Path]:
        """Build a list containing absolute paths to the generated files."""
        return [path for path in Path(root_dir).glob("*") if path.is_file()]

    return func


@pytest.fixture(scope="session")
def cutter_result(cookies_session, context):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context)
