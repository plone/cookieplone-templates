"""Test cookiecutter generation with all features enabled."""

from pathlib import Path

import pytest


def test_creation(cookies, template_path, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == "app"
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
        [".github", False],
        ["_project_files", False],
        ["packages/aurora-addon", False],
        ["mrs.developer.json", True],
        ["pnpm-workspace.yaml", True],
    ],
)
def test_paths(cutter_result, file_path: str, exists: bool):
    """Check the add-on and the template files are not generated."""
    path = cutter_result.project_path / file_path
    assert path.exists() is exists


@pytest.mark.parametrize(
    "file_path,text,expected",
    [
        ["Makefile", "aurora-addon", False],
        ["package.json", "aurora-addon", False],
        ["package.json", "project-dev", True],
        ["registry.config.ts", "aurora-addon", False],
        ["registry.config.ts", "addons.push", False],
        ["mrs.developer.json", '"tag": "1.0.0-alpha.19"', True],
    ],
)
def test_root_files_do_not_mention_addon(
    cutter_result, file_path: Path, text: str, expected: bool
):
    """Check if root files were generated and have no reference to the addon."""
    path = cutter_result.project_path / file_path
    assert path.exists()
    assert path.is_file()
    assert (text in path.read_text()) is expected
