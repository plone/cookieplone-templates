"""Test cookiecutter generation with all features enabled."""

import pytest


def test_creation(cookies, template_path, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == ".github"
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


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        ["workflows/backend.yml", "github-workflow"],
        ["workflows/frontend.yml", "github-workflow"],
        ["workflows/config.yml", "github-workflow"],
        ["workflows/docs.yml", "github-workflow"],
        ["workflows/main.yml", "github-workflow"],
        ["workflows/manual_deploy.yml", "github-workflow"],
        ["workflows/rtd-pr-preview.yml", "github-workflow"],
        ["workflows/varnish.yml", "github-workflow"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)


@pytest.mark.parametrize(
    "file_path",
    [
        "workflows/backend.yml",
        "workflows/frontend.yml",
        "workflows/config.yml",
        "workflows/docs.yml",
        "workflows/main.yml",
        "workflows/manual_deploy.yml",
        "workflows/rtd-pr-preview.yml",
        "workflows/varnish.yml",
    ],
)
def test_created_files(cutter_result, file_path: str):
    path = (cutter_result.project_path / file_path).resolve()
    assert path.exists()
    assert path.is_file()
