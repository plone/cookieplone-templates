"""Test cookiecutter generation with all features enabled."""

import pytest

GITHUB_ACTIONS = [
    ".github/workflows/backend.yml",
    ".github/workflows/changelog.yml",
    ".github/workflows/config.yml",
    ".github/workflows/frontend.yml",
    ".github/workflows/main.yml",
]

GITHUB_INSTRUCTIONS = [
    ".github/instructions/docs.instructions.md",
    ".github/instructions/volto.instructions.md",
]

VSCODE_SETTINGS = [
    ".vscode/extensions.json",
    ".vscode/launch.json",
    ".vscode/settings.json",
]

BACKEND_FILES = [
    "backend/.gitignore",
    "backend/CHANGELOG.md",
    "backend/CONTRIBUTORS.md",
    "backend/instance.yaml",
    "backend/LICENSE.GPL",
    "backend/LICENSE.md",
    "backend/Makefile",
    "backend/mx.ini",
    "backend/pyproject.toml",
    "backend/README.md",
    "backend/scripts/create_site.py",
    "backend/src/collective/addon/__init__.py",
    "backend/src/collective/addon/configure.zcml",
    "backend/src/collective/addon/content/__init__.py",
    "backend/src/collective/addon/controlpanels/__init__.py",
    "backend/src/collective/addon/controlpanels/configure.zcml",
    "backend/src/collective/addon/dependencies.zcml",
    "backend/src/collective/addon/indexers/__init__.py",
    "backend/src/collective/addon/indexers/configure.zcml",
    "backend/src/collective/addon/locales/__init__.py",
    "backend/src/collective/addon/locales/__main__.py",
    "backend/src/collective/addon/locales/collective.addon.pot",
    "backend/src/collective/addon/profiles/default/browserlayer.xml",
    "backend/src/collective/addon/profiles/default/catalog.xml",
    "backend/src/collective/addon/profiles/default/controlpanel.xml",
    "backend/src/collective/addon/profiles/default/diff_tool.xml",
    "backend/src/collective/addon/profiles/default/metadata.xml",
    "backend/src/collective/addon/profiles/default/repositorytool.xml",
    "backend/src/collective/addon/profiles/default/rolemap.xml",
    "backend/src/collective/addon/profiles/default/types.xml",
    "backend/src/collective/addon/profiles/default/types/.gitkeep",
    "backend/src/collective/addon/profiles/uninstall/browserlayer.xml",
    "backend/src/collective/addon/serializers/__init__.py",
    "backend/src/collective/addon/serializers/configure.zcml",
    "backend/src/collective/addon/setuphandlers/__init__.py",
    "backend/src/collective/addon/testing.py",
    "backend/src/collective/addon/upgrades/__init__.py",
    "backend/src/collective/addon/upgrades/configure.zcml",
    "backend/src/collective/addon/vocabularies/__init__.py",
    "backend/src/collective/addon/vocabularies/configure.zcml",
]

FRONTEND_FILES = [
    "frontend/.storybook/main.js",
    "frontend/.storybook/preview.jsx",
    "frontend/cypress/support/commands.js",
    "frontend/cypress/support/e2e.js",
    "frontend/cypress/tests/.gitkeep",
    "frontend/cypress/tests/example.cy.js",
    "frontend/cypress/.gitkeep",
    "frontend/.eslintrc.js",
    "frontend/.gitignore",
    "frontend/.npmignore",
    "frontend/.npmrc",
    "frontend/.prettierignore",
    "frontend/.prettierrc",
    "frontend/.stylelintrc",
    "frontend/cypress.config.js",
    "frontend/jest-addon.config.js",
    "frontend/Makefile",
    "frontend/mrs.developer.json",
    "frontend/package.json",
    "frontend/pnpm-workspace.yaml",
    "frontend/README.md",
    "frontend/volto.config.js",
]


ROOT_FILES = [
    *GITHUB_ACTIONS,
    *GITHUB_INSTRUCTIONS,
    *VSCODE_SETTINGS,
    *BACKEND_FILES,
    *FRONTEND_FILES,
]


def test_creation(cookies, template_path, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context["project_slug"]
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
    "file_path",
    ROOT_FILES,
)
def test_root_files_generated(cutter_result, file_path):
    """Check if root files were generated."""
    path = cutter_result.project_path / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        [".github/workflows/backend.yml", "github-workflow"],
        [".github/workflows/frontend.yml", "github-workflow"],
        [".github/workflows/changelog.yml", "github-workflow"],
        [".github/workflows/config.yml", "github-workflow"],
        [".github/workflows/main.yml", "github-workflow"],
        ["backend/pyproject.toml", "pyproject"],
        ["frontend/package.json", "package"],
        ["frontend/packages/volto-addon/package.json", "package"],
        ["frontend/packages/volto-addon/tsconfig.json", "tsconfig"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)
