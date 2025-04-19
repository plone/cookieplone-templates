"""Test cookiecutter generation with all features enabled."""

import pytest

GITHUB_ACTIONS = [
    ".github/workflows/acceptance.yml",
    ".github/workflows/changelog.yml",
    ".github/workflows/code.yml",
    ".github/workflows/i18n.yml",
    ".github/workflows/storybook.yml",
    ".github/workflows/unit.yml",
]


ROOT_FILES = [
    *GITHUB_ACTIONS,
    ".storybook/main.js",
    ".storybook/preview.jsx",
    "cypress/support/commands.js",
    "cypress/support/e2e.js",
    "cypress/tests/.gitkeep",
    "cypress/tests/example.cy.js",
    "cypress/.gitkeep",
    ".eslintrc.js",
    ".gitignore",
    ".npmignore",
    ".npmrc",
    ".prettierignore",
    ".prettierrc",
    ".stylelintrc",
    "cypress.config.js",
    "jest-addon.config.js",
    "Makefile",
    "mrs.developer.json",
    "package.json",
    "pnpm-workspace.yaml",
    "README.md",
    "volto.config.js",
]


PKG_SRC_FILES = [
    ".gitignore",
    ".release-it.json",
    "babel.config.js",
    "CHANGELOG.md",
    "locales/de/LC_MESSAGES/volto.po",
    "locales/en/LC_MESSAGES/volto.po",
    "locales/es/LC_MESSAGES/volto.po",
    "locales/pt_BR/LC_MESSAGES/volto.po",
    "locales/volto.pot",
    "news/.gitkeep",
    "package.json",
    "src/components/.gitkeep",
    "src/index.js",
    "towncrier.toml",
    "tsconfig.json",
]


def test_creation(cookies, template_path, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context["frontend_addon_name"]
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


@pytest.mark.parametrize("file_path", PKG_SRC_FILES)
def test_pkg_src_files_generated(cutter_result, file_path: str):
    """Check if package files were generated."""
    package_name = cutter_result.context["frontend_addon_name"]
    src_path = cutter_result.project_path / "packages" / package_name
    path = src_path / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        [".github/workflows/acceptance.yml", "github-workflow"],
        [".github/workflows/changelog.yml", "github-workflow"],
        [".github/workflows/code.yml", "github-workflow"],
        [".github/workflows/i18n.yml", "github-workflow"],
        [".github/workflows/storybook.yml", "github-workflow"],
        [".github/workflows/unit.yml", "github-workflow"],
        ["package.json", "package"],
        ["packages/volto-addon/package.json", "package"],
        ["packages/volto-addon/tsconfig.json", "tsconfig"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)
