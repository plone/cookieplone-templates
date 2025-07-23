"""Test Generator: GitLab CI/CD config"""

import pytest


GITLAB_FILES = [
    ".gitlab-ci.yml",
]


@pytest.mark.parametrize("filepath", GITLAB_FILES)
def test_project_gitlab_files(cutter_devops_result_gitlab, filepath: str):
    """Test created files."""
    folder = cutter_devops_result_gitlab.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize("filepath", GITLAB_FILES)
def test_project_no_gitlab_files(cutter_devops_result_no_gitlab, filepath: str):
    """Test Cache-related files are not present."""
    folder = cutter_devops_result_no_gitlab.project_path
    path = folder / filepath
    assert path.exists() is False

