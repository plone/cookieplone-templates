"""Test cookiecutter generation with all features enabled."""

from pathlib import Path

import pytest


def test_creation(cookies, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == "project-title"
    assert result.project_path.is_dir()


def test_variable_substitution(build_files_list, variable_pattern, cutter_result):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        for line in open(path):
            match = variable_pattern.search(line)
            msg = f"cookiecutter variable not replaced in {path}"
            assert match is None, msg


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        [".github/workflows/varnish.yml", "github-workflow"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)


@pytest.mark.parametrize(
    "file_path",
    [
        ".github/workflows/varnish.yml",
        "backend/src/project/title/profiles/default/registry/plone.cachepurging.interfaces.ICachePurgingSettings.xml",  # noQA
        "backend/src/project/title/profiles/default/registry/plone.caching.interfaces.ICacheSettings.xml",  # noQA
        "devops/varnish/etc/varnish.vcl",
        "devops/varnish/Dockerfile",
    ],
)
def test_created_files(cutter_result, file_path: str):
    path = (cutter_result.project_path / file_path).resolve()
    assert path.exists()
    assert path.is_file()
