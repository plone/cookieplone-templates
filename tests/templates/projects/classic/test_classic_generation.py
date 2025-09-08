"""Test Generator: ./"""

import json

import pytest


@pytest.mark.parametrize(
    "filepath",
    [
        ".editorconfig",
        ".gitignore",
        ".vscode/extensions.json",
        ".vscode/settings.json",
        "dependabot.yml",
        "CHANGELOG.md",
        "Makefile",
        "README.md",
        "repository.toml",
        "version.txt",
    ],
)
def test_project_files(cutter_result, filepath: str):
    """Test created files."""
    folder = cutter_result.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        [".github/workflows/backend.yml", "github-workflow"],
        [".github/workflows/docs.yml", "github-workflow"],
        [".github/workflows/main.yml", "github-workflow"],
        [".github/workflows/manual_deploy.yml", "github-workflow"],
        [".github/workflows/rtd-pr-preview.yml", "github-workflow"],
        [".github/workflows/varnish.yml", "github-workflow"],
        ["docker-compose.yml", "docker-compose"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)


@pytest.mark.parametrize(
    "file_path,bad_url",
    [
        ["README.md", "https://github.com/plonegovbr/plonegov.ploneorgbr"],
        ["README.md", "https://github.com/plonegovbr/volto-ploneorgbr"],
        ["backend/README.md", "https://github.com/plonegovbr/plonegov.ploneorgbr"],
        ["backend/pyproject.toml", "https://github.com/plonegovbr/plonegov.ploneorgbr"],
    ],
)
def test_repository_url(cutter_result, file_path: str, bad_url: str):
    path = cutter_result.project_path / file_path
    assert bad_url not in path.read_text()
