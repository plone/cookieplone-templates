"""Test Generator: ./"""

import json

import pytest


@pytest.mark.parametrize(
    "filepath",
    [
        ".editorconfig",
        ".gitignore",
        ".vscode/settings.json",
        "dependabot.yml",
        "CHANGELOG.md",
        "Makefile",
        "README.md",
        "version.txt",
    ],
)
def test_project_files(cutter_result, filepath: str):
    """Test created files."""
    folder = cutter_result.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize(
    "filepath",
    [
        "frontend/mrs.developer.json",
        "frontend/package.json",
    ],
)
def test_valid_json_files(cutter_result, filepath: str):
    """Test generated json files are valid."""
    folder = cutter_result.project_path
    path = folder / filepath
    with open(path, "r") as fh:
        content = json.load(fh)
    assert content


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        [".github/workflows/backend.yml", "github-workflow"],
        [".github/workflows/frontend.yml", "github-workflow"],
        [".github/workflows/manual_deploy.yml", "github-workflow"],
        [".github/workflows/varnish.yml", "github-workflow"],
        [".pre-commit-config.yaml", "pre-commit-config"],
        ["backend/.pre-commit-config.yaml", "pre-commit-config"],
        ["frontend/.pre-commit-config.yaml", "pre-commit-config"],
        ["docker-compose.yml", "docker-compose"],
        ["frontend/package.json", "package"],
        ["frontend/packages/volto-ploneorgbr/package.json", "package"],
        ["frontend/packages/volto-ploneorgbr/tsconfig.json", "tsconfig"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)
