"""Test cookieplone generation."""

import json

import pytest


def test_creation(cookies, template_path, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == ".vscode"
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
    "file_path,exists",
    [
        ["extensions.json", True],
        ["launch.json", True],
        ["settings.json", True],
    ],
)
def test_created_files(cutter_result, load_json, file_path: str, exists: bool):
    path = (cutter_result.project_path / file_path).resolve()
    assert path.exists() is exists
    if exists:
        assert path.is_file()
        content = load_json(path)  # valid JSON
        assert isinstance(content, dict)


@pytest.mark.parametrize(
    "file_path,path,expected",
    [
        [
            "launch.json",
            "configurations/0/program",
            "${workspaceFolder}/backend/.venv/bin/runwsgi",
        ],
        [
            "launch.json",
            "configurations/0/cwd",
            "${workspaceFolder}/backend",
        ],
        [
            "settings.json",
            "python.testing.pytestArgs/0",
            "backend/tests",
        ],
        [
            "settings.json",
            "eslint.workingDirectories/0",
            "./frontend",
        ],
    ],
)
def test_settings(
    cutter_result, load_json, traverse, file_path: str, path: str, expected: str
):
    data = load_json((cutter_result.project_path / file_path).resolve())  # valid JSON
    result = traverse(data, path)
    assert result == expected
