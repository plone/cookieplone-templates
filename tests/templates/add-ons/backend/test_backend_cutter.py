"""Test cookiecutter generation with all features enabled."""

from pathlib import Path

import pytest


def test_creation(cookies, template_path, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context["python_package_name"]
    assert result.project_path.is_dir()


def test_variable_substitution(build_files_list, variable_pattern, cutter_result):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        with open(path) as fh:
            for line in fh:
                match = {pattern.search(line) for pattern in variable_pattern}
                msg = f"cookiecutter variable not replaced in {path}"
                assert match == {None}, msg


def test_root_files_generated(cutter_result, root_file_path):
    """Check if root files were generated."""
    path = cutter_result.project_path / root_file_path
    assert path.exists()
    assert path.is_file()


def test_pkg_src_files_generated(cutter_result, pkg_file_path: str):
    """Check if distribution files were generated."""
    package_path = cutter_result.context["__package_path"]
    src_path = cutter_result.project_path / "src" / package_path
    path = src_path / pkg_file_path
    assert path.exists()
    assert path.is_file()


def test_pkg_src_feature_files_generated(cutter_result, pkg_file_path_headless: str):
    """Check if feature-specific files were generated."""
    package_path = cutter_result.context["__package_path"]
    src_path = cutter_result.project_path / "src" / package_path
    path = src_path / pkg_file_path_headless
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
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


def test_git_initialization_not_set(cookies, template_path, context_no_git):
    from cookieplone.utils import git

    cutter_result = cookies.bake(extra_context=context_no_git, template=template_path)
    path = cutter_result.project_path
    assert git.check_path_is_repository(path) is False


def test_pkg_src_files_generated_without_namespace(
    cutter_result_no_namespace, pkg_file_path: str
):
    """Check package contents with no namespaces."""
    src_path = cutter_result_no_namespace.project_path / "src/addon"
    path = src_path / pkg_file_path
    assert path.exists()
    assert path.is_file()


def test_pkg_src_files_generated_with_two_namespaces(
    cutter_result_two_namespaces, pkg_file_path: str
):
    """Check package contents with 2 namespaces."""
    src_path = cutter_result_two_namespaces.project_path / "src/foo/bar/baz"
    path = src_path / pkg_file_path
    assert path.exists()
    assert path.is_file()
