"""Test cookiecutter generation with all features enabled."""

import json

import pytest


def test_creation(cookies, template_path, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == "project-title"
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


GENERATED_FILES = [
    "backend/.dockerignore",
    "backend/Dockerfile.acceptance",
    "backend/Dockerfile",
    "backend/Makefile",
    "backend/scripts/create_site.py",
    "backend/src/packagename/locales/__init__.py",
    "backend/src/packagename/locales/en/LC_MESSAGES/project.title.po",
    "backend/src/packagename/locales/project.title.pot",
    "backend/src/packagename/locales/__main__.py",
    "backend/src/packagename/profiles/default/registry/plone.base.interfaces.controlpanel.IMailSchema.xml",
    "backend/src/packagename/profiles/default/registry/plone.base.interfaces.controlpanel.ISiteSchema.xml",
    "backend/src/packagename/profiles/default/registry/plone.i18n.interfaces.ILanguageSchema.xml",
    "backend/src/packagename/profiles/initial/metadata.xml",
    "backend/src/packagename/setuphandlers/examplecontent/.gitkeep",
    "backend/src/packagename/setuphandlers/examplecontent/content/__metadata__.json",
    "backend/src/packagename/setuphandlers/examplecontent/content/a58ccead718140c1baa98d43595fc3e6/data.json",
    "backend/src/packagename/setuphandlers/examplecontent/content/a58ccead718140c1baa98d43595fc3e6/image/plone-foundation.png",
    "backend/src/packagename/setuphandlers/examplecontent/content/a720393b3c0240e5bd27c43fcd2cfd1e/data.json",
    "backend/src/packagename/setuphandlers/examplecontent/content/plone_site_root/data.json",
    "backend/src/packagename/setuphandlers/examplecontent/discussions.json",
    "backend/src/packagename/setuphandlers/examplecontent/portlets.json",
    "backend/src/packagename/setuphandlers/examplecontent/principals.json",
    "backend/src/packagename/setuphandlers/examplecontent/redirects.json",
    "backend/src/packagename/setuphandlers/examplecontent/relations.json",
    "backend/src/packagename/setuphandlers/examplecontent/translations.json",
    "backend/src/packagename/setuphandlers/initial.py",
    "frontend/.dockerignore",
    "frontend/Dockerfile",
    "frontend/Makefile",
    "frontend/packages/volto-project-title/src/index.js",
]


@pytest.mark.parametrize("file_path", GENERATED_FILES)
def test_created_files(cutter_result, file_path: str):
    path = (cutter_result.project_path / file_path).resolve()
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize(
    "file_path", [f for f in GENERATED_FILES if f.endswith(".json")]
)
def test_json_files_are_valid(cutter_result, file_path: str):
    path = (cutter_result.project_path / file_path).resolve()
    result = json.loads(path.read_text())
    assert isinstance(result, dict | list)
