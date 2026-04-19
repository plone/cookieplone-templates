"""Test cookiecutter generation for plone7_nick_embedded."""

import pytest

GITHUB_WORKFLOWS = [
    ".github/workflows/acceptance.yml",
    ".github/workflows/changelog.yml",
    ".github/workflows/code.yml",
    ".github/workflows/i18n.yml",
    ".github/workflows/storybook.yml",
    ".github/workflows/unit.yml",
]


ROOT_FILES = [
    *GITHUB_WORKFLOWS,
    ".storybook/main.js",
    ".storybook/preview.jsx",
    ".gitignore",
    ".npmignore",
    ".npmrc",
    ".pnpmfile.cjs",
    ".prettierignore",
    ".prettierrc",
    ".stylelintrc",
    "Dockerfile",
    "eslint.config.mjs",
    "Makefile",
    "mrs.developer.json",
    "package.json",
    "pnpm-workspace.yaml",
    "README.md",
    "registry.config.ts",
]


PKG_SRC_FILES = [
    ".gitignore",
    ".release-it.json",
    "CHANGELOG.md",
    "config/server.ts",
    "index.ts",
    "locales/de/LC_MESSAGES/volto.po",
    "locales/en/LC_MESSAGES/volto.po",
    "locales/volto.pot",
    "news/.gitkeep",
    "package.json",
    "public/.gitkeep",
    "towncrier.toml",
    "tsconfig.json",
    "types.d.ts",
    "vite.extend.ts",
]


PKG_NICK_FILES = [
    "package.json",
    "profiles/default/metadata.json",
    "profiles/default/users.json",
    "profiles/default/groups.json",
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


@pytest.mark.parametrize("file_path", ROOT_FILES)
def test_root_files_generated(cutter_result, file_path: str):
    """Check if root files were generated."""
    path = cutter_result.project_path / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize("file_path", PKG_SRC_FILES)
def test_pkg_src_files_generated(cutter_result, file_path: str):
    """Check if add-on package files were generated."""
    package_name = cutter_result.context["frontend_addon_name"]
    path = cutter_result.project_path / "packages" / package_name / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize("file_path", PKG_NICK_FILES)
def test_pkg_nick_files_generated(cutter_result, file_path: str):
    """Check if -nick companion package files were generated."""
    package_name = f"{cutter_result.context['frontend_addon_name']}-nick"
    path = cutter_result.project_path / "packages" / package_name / file_path
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
        ["packages/{package_name}/package.json", "package"],
        ["packages/{package_name}/tsconfig.json", "tsconfig"],
        ["packages/{package_name}-nick/package.json", "package"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    package_name = cutter_result.context["frontend_addon_name"]
    path = cutter_result.project_path / file_path.format(package_name=package_name)
    assert schema_validate_file(path, schema_name)
