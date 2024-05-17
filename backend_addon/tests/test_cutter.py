"""Test cookiecutter generation with all features enabled."""

from pathlib import Path

import pytest

from .conftest import PKG_SRC_FEATURE_HEADLESS, PKG_SRC_FILES, ROOT_FILES


def test_creation(cookies, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context["python_package_name"]
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
    package_namespace = cutter_result.context["__package_namespace"]
    package_name = cutter_result.context["__package_name"]
    file_path = file_path.format(package_name=package_name)
    src_path = cutter_result.project_path / "src" / package_namespace / package_name
    path = src_path / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize("file_path", PKG_SRC_FEATURE_HEADLESS)
def test_pkg_src_feature_files_generated(cutter_result, file_path: str):
    """Check if feature-specific files were generated."""
    package_namespace = cutter_result.context["__package_namespace"]
    package_name = cutter_result.context["__package_name"]
    src_path = cutter_result.project_path / "src" / package_namespace / package_name
    path = src_path / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        [".github/workflows/meta.yml", "github-workflow"],
        [".pre-commit-config.yaml", "pre-commit-config"],
        ["pyproject.toml", "pyproject"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)


def test_git_initialization(cutter_result):
    from cookieplone.utils import git

    path = cutter_result.project_path
    repo = git.repo_from_path(path)
    assert Path(repo.working_dir) == path


def test_git_initialization_not_set(cookies, context_no_git):
    from cookieplone.utils import git

    cutter_result = cookies.bake(extra_context=context_no_git)
    path = cutter_result.project_path
    assert git.check_path_is_repository(path) is False
