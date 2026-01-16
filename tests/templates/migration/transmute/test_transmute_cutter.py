"""Test cookiecutter generation with all features enabled."""

from pathlib import Path


def test_creation(cookies, template_path, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()


def test_git_initialization(cutter_result):
    from cookieplone.utils import git

    path = cutter_result.project_path
    repo = git.repo_from_path(path)
    assert Path(repo.working_dir) == path


def test_files_generated(cutter_result, root_file_path):
    """Check if files were generated."""
    path = cutter_result.project_path / root_file_path
    assert path.exists()
    assert path.is_file()


def test_folders_generated(cutter_result, root_folder_path):
    """Check if folders were generated."""
    path = cutter_result.project_path / root_folder_path
    assert path.exists()
    assert path.is_dir()
