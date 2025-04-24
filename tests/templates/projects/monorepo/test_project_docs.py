"""Test Generator: /devops."""

import pytest
import yaml

DOCS_FOLDER_FILES = [
    ".readthedocs.yml",
    "docs/.gitignore",
    "docs/.vale.ini",
    "docs/docs/_static/favicon.ico",
    "docs/docs/_static/logo.svg",
    "docs/docs/_templates/404.html",
    "docs/docs/concepts/index.md",
    "docs/docs/conf.py",
    "docs/docs/glossary.md",
    "docs/docs/how-to-guides/index.md",
    "docs/docs/index.md",
    "docs/docs/reference/index.md",
    "docs/docs/robots.txt",
    "docs/docs/tutorials/index.md",
    "docs/Makefile",
    "docs/pyproject.toml",
    "docs/README.md",
    "docs/styles/config/vocabularies/Base/accept.txt",
    "docs/styles/config/vocabularies/Base/reject.txt",
    "docs/styles/config/vocabularies/Plone/accept.txt",
    "docs/styles/config/vocabularies/Plone/reject.txt",
]

GHA_ACTIONS_CI = [
    ".github/workflows/docs.yml",
    ".github/workflows/rtd-pr-preview.yml",
]


DOCS_FILES = DOCS_FOLDER_FILES + GHA_ACTIONS_CI


@pytest.mark.parametrize("filepath", DOCS_FILES)
def test_project_docs_files(cutter_result, filepath: str):
    """Test created files."""
    folder = cutter_result.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize(
    "filepath",
    [filepath for filepath in DOCS_FILES if filepath.endswith(".yml")],
)
def test_valid_yaml_files(cutter_result, filepath: str):
    """Test generated yaml files are valid."""
    folder = cutter_result.project_path
    path = folder / filepath
    with open(path) as fh:
        content = yaml.full_load(fh)
    assert content


@pytest.mark.parametrize("filepath", DOCS_FILES)
def test_project_no_docs(cutter_result_no_docs, filepath: str):
    """Test no documentation file is present."""
    folder = cutter_result_no_docs.project_path
    path = folder / filepath
    assert path.exists() is False


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        ["docs/pyproject.toml", "pyproject"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        [".github/workflows/main.yml", "github-workflow"],
    ],
)
def test_json_schema_no_docs(
    cutter_result_no_docs, schema_validate_file, file_path: str, schema_name: str
):
    """Validate the GHA workflows are valid even when no docs are generated."""
    path = cutter_result_no_docs.project_path / file_path
    assert schema_validate_file(path, schema_name)
