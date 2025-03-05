"""Test cookiecutter generation for documentation_addon."""

from pathlib import Path

import pytest

from .conftest import DOCS_FILES, ROOT_FILES


def test_creation(cookies, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context["__folder_name"]
    assert result.project_path.is_dir()


def test_variable_substitution(build_files_list, variable_pattern, cutter_result):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        # Skip binary files in _static/
        if path.suffix in [".ico", ".svg"]:
            continue
        for line in open(path, encoding="utf-8"):
            match = variable_pattern.search(line)
            msg = f"cookiecutter variable not replaced in {path}"
            assert match is None, msg


@pytest.mark.parametrize("file_path", ROOT_FILES)
def test_root_files_generated(cutter_result, file_path):
    """Check if root files were generated."""
    path = cutter_result.project_path / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize("file_path", DOCS_FILES)
def test_docs_files_generated(cutter_result, file_path):
    """Check if documentation files were generated."""
    docs_path = cutter_result.project_path / "docs"
    path = docs_path / file_path
    assert path.exists()
    assert path.is_file()


def test_git_initialization(cutter_result):
    """Check if Git repository is initialized when enabled."""
    from cookieplone.utils import git

    path = cutter_result.project_path
    repo = git.repo_from_path(path)
    assert Path(repo.working_dir) == path


def test_git_initialization_not_set(cutter_result_no_git):
    """Check if Git repository is not initialized when disabled."""
    from cookieplone.utils import git

    path = cutter_result_no_git.project_path
    assert not git.check_path_is_repository(path)


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        ["pyproject.toml", "pyproject"],
    ],
)
def test_json_schema(cutter_result, schema_validate_file, file_path: str, schema_name: str):
    """Check if specific files match their JSON schemas."""
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)
