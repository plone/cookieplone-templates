"""Test Generator: /backend."""

from pathlib import Path

import pytest

BACKEND_FILES = [
    ".dockerignore",
    ".gitignore",
    "Dockerfile.acceptance",
    "Dockerfile",
    "instance.yaml",
    "Makefile",
    "mx.ini",
    "pyproject.toml",
    "version.txt",
]


@pytest.mark.parametrize("filename", BACKEND_FILES)
def test_backend_top_level_files(cutter_result, filename: str):
    """Test backend files."""
    backend_folder = cutter_result.project_path / "backend"
    path = backend_folder / filename
    assert path.is_file()


BACKEND_PACKAGE_FILES_PYTEST = [
    "src/plonegov/ploneorgbr/configure.zcml",
    "src/plonegov/ploneorgbr/dependencies.zcml",
    "src/plonegov/ploneorgbr/permissions.zcml",
    "src/plonegov/ploneorgbr/profiles.zcml",
    "src/plonegov/ploneorgbr/profiles/initial/metadata.xml",
    "src/plonegov/ploneorgbr/setuphandlers/initial.py",
    "src/plonegov/ploneorgbr/setuphandlers/examplecontent/.gitkeep",
    "src/plonegov/ploneorgbr/testing.py",
    "tests/conftest.py",
    "tests/setup/test_setup_install.py",
    "tests/setup/test_setup_uninstall.py",
]


@pytest.mark.parametrize("filename", BACKEND_FILES)
def test_backend_package_files_pytest(cutter_result, filename: str):
    """Test backend files."""
    backend_folder = cutter_result.project_path / "backend"
    path = backend_folder / filename
    assert path.is_file()


FILES_TO_BE_REMOVED = [
    ".github",
    ".git",
    ".meta.toml",
]


@pytest.mark.parametrize("filename", FILES_TO_BE_REMOVED)
def test_backend_package_files_removed(cutter_result, filename: str):
    """Test backend package files are removed."""
    backend_folder = cutter_result.project_path / "backend"
    path = backend_folder / filename
    assert path.exists() is False
    assert path.parent.exists()


BACKEND_HEADLESS_FILE_CHECKS = [
    ["pyproject.toml", "plone.volto"],
    ["pyproject.toml", "plone.restapi"],
    ["src/plonegov/ploneorgbr/dependencies.zcml", "plone.volto"],
    ["src/plonegov/ploneorgbr/dependencies.zcml", "plone.restapi"],
    ["src/plonegov/ploneorgbr/profiles/default/metadata.xml", "plone.volto:default"],
]


@pytest.mark.parametrize("filename,content", BACKEND_HEADLESS_FILE_CHECKS)
def test_backend_headless_support(cutter_result, filename: str, content: str):
    """Test backend files contain headless support."""
    backend_folder = cutter_result.project_path / "backend"
    path = backend_folder / filename
    assert path.is_file()
    assert content in path.read_text()


def test_git_repo_is_the_project(cutter_result):
    from cookieplone.utils import git

    path = cutter_result.project_path
    backend_path = path / "backend"
    repo = git.repo_from_path(path)
    assert Path(repo.working_dir) != backend_path
    assert Path(repo.working_dir) == path
