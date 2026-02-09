"""Test cookieplone generation."""

import json

import pytest


@pytest.fixture(scope="session")
def context(context_monorepo_addon):
    return context_monorepo_addon


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
def test_created_files(cutter_result, file_path: str, exists: bool):
    path = (cutter_result.project_path / file_path).resolve()
    assert path.exists() is exists
    if exists:
        assert path.is_file()
        content = json.loads(path.read_text())  # valid JSON
        assert isinstance(content, dict)
