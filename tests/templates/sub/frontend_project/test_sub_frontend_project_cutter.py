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
    "file_path,text,expected",
    [
        [".eslintrc.js", "volto-addon", False],
        ["Makefile", "volto-addon", False],
        ["package.json", "volto-addon-dev", False],
        ["package.json", "project-dev", True],
        ["volto.config.js", "volto-addon", False],
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
