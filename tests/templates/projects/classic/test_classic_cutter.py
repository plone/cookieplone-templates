
"""Test cookiecutter generation."""

from pathlib import Path

import pytest


def build_files_list(root_dir: Path) -> list[Path]:
    """Build a list containing absolute paths to the generated files."""
    return [path for path in Path(root_dir).glob("*") if path.is_file()]


def test_default_configuration(cookies, template_path, context: dict):
    """Generated project should replace all variables."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()


def test_variable_substitution(cutter_result, variable_pattern):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        with open(path) as fh:
            for line in fh:
                match = {pattern.search(line) for pattern in variable_pattern}
                msg = f"cookiecutter variable not replaced in {path}"
                assert match == {None}, msg


FOLDERS = [
    ".github",
    ".vscode",
    "backend",
    "devops",
]


@pytest.mark.parametrize("folder_name", FOLDERS)
def test_root_folders(cutter_result, folder_name: str):
    """Test folders were created."""
    folder = cutter_result.project_path / folder_name
    assert folder.is_dir()


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
