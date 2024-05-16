"""Test Generator: /backend."""

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
    "requirements-docker.txt",
    "requirements.txt",
    "version.txt",
]


@pytest.mark.parametrize("filename", BACKEND_FILES)
def test_backend_top_level_files(cutter_result, filename: str):
    """Test backend files."""
    backend_folder = cutter_result.project_path / "backend"
    path = backend_folder / filename
    assert path.is_file()


BACKEND_PACKAGE_FILES_PYTEST = [
    "src/ploneorgbr/setup.py",
    "src/plonegov/ploneorgbr/configure.zcml",
    "src/plonegov/ploneorgbr/dependencies.zcml",
    "src/plonegov/ploneorgbr/permissions.zcml",
    "src/plonegov/ploneorgbr/profiles.zcml",
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
]


@pytest.mark.parametrize("filename", FILES_TO_BE_REMOVED)
def test_backend_package_files_removed(cutter_result, filename: str):
    """Test backend package files are removed."""
    backend_folder = cutter_result.project_path / "backend"
    path = backend_folder / filename
    assert path.exists() is False
    assert path.parent.exists()
