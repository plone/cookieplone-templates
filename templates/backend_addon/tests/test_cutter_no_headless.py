"""Test cookiecutter generation without headless feature."""

import pytest

from .conftest import PKG_SRC_FEATURE_HEADLESS, PKG_SRC_FILES, ROOT_FILES


@pytest.fixture(scope="session")
def cutter_result(cookies_session, context_no_headless):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context_no_headless)


def test_creation(cookies, context_no_headless: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context_no_headless)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context_no_headless["python_package_name"]
    assert result.project_path.is_dir()


def test_variable_substitution(build_files_list, variable_pattern, cutter_result):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        for line in open(path):
            match = variable_pattern.search(line)
            msg = f"cookiecutter variable not replaced in {path}"
            assert match is None, msg


@pytest.mark.parametrize(
    "file_path",
    ROOT_FILES,
)
def test_root_files_generated(cutter_result, file_path):
    """Check if root files were generated."""
    path = cutter_result.project_path / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize("file_path", PKG_SRC_FILES)
def test_pkg_src_files_generated(cutter_result, file_path: str):
    """Check if distribution files were generated."""
    package_path = cutter_result.context["__package_path"]
    src_path = cutter_result.project_path / "src" / package_path
    path = src_path / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize("file_path", PKG_SRC_FEATURE_HEADLESS)
def test_pkg_src_headless_files_not_generated(cutter_result, file_path: str):
    """Check feature-specific files were not generated."""
    package_path = cutter_result.context["__package_path"]
    src_path = cutter_result.project_path / "src" / package_path
    path = src_path / file_path
    assert path.exists() is False
