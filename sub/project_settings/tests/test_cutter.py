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
    "file_path",
    [
        "backend/src/project/title/locales/__init__.py",
        "backend/src/project/title/locales/en/LC_MESSAGES/project.title.po",
        "backend/src/project/title/locales/project.title.pot",
        "backend/src/project/title/locales/update.py",
        "backend/src/project/title/profiles/default/registry/plone.base.interfaces.controlpanel.IMailSchema.xml",  # noQA
        "backend/src/project/title/profiles/default/registry/plone.base.interfaces.controlpanel.ISiteSchema.xml",  # noQA
        "backend/src/project/title/profiles/default/registry/plone.i18n.interfaces.ILanguageSchema.xml",
        "frontend/.dockerignore",
        "frontend/Dockerfile",
        "frontend/Makefile",
        "frontend/packages/volto-project-title/src/index.js",
    ],
)
def test_created_files(cutter_result, file_path: str):
    path = (cutter_result.project_path / file_path).resolve()
    assert path.exists()
    assert path.is_file()
