"""Test cookiecutter generation for volto_nick."""

import json

import pytest
import tomli

ROOT_FILES = [
    ".editorconfig",
    ".gitignore",
    "CHANGELOG.md",
    "Makefile",
    "README.md",
    "dependabot.yml",
    "repository.toml",
    "towncrier.toml",
    "version.txt",
]

BACKEND_FILES = [
    ".gitignore",
    ".prettierignore",
    "Makefile",
    "README.md",
    "babel.config.json",
    "config.ts",
    "eslint.config.ts",
    "knexfile.ts",
    "mrs.developer.json",
    "package.json",
    "pnpm-workspace.yaml",
    "tsconfig.json",
]

BACKEND_PROJECT_FILES = [
    "src/events/index.ts",
    "src/migrations/.keep",
    "src/profiles/default/documents/_root.json",
    "src/profiles/default/groups.json",
    "src/profiles/default/metadata.json",
    "src/profiles/default/users.json",
]

CI_FILES = [
    "dependabot.yml",
    "workflows/backend.yml",
    "workflows/changelog.yml",
    "workflows/config.yml",
    "workflows/frontend.yml",
    "workflows/main.yml",
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


@pytest.mark.parametrize("file_path", ROOT_FILES)
def test_root_files_generated(cutter_result, file_path: str):
    """Check if root files were generated."""
    path = cutter_result.project_path / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize("file_path", BACKEND_FILES + BACKEND_PROJECT_FILES)
def test_backend_files_generated(cutter_result, file_path: str):
    """Check if Nick backend files were generated below backend/."""
    path = cutter_result.project_path / "backend" / file_path
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize(
    "file_path",
    [
        ".pnpmfile.cjs",
        "Makefile",
        "package.json",
        "pnpm-workspace.yaml",
        "packages/volto-plone/package.json",
    ],
)
def test_frontend_files_generated(cutter_result, file_path: str):
    """Check if the Volto frontend workspace was generated."""
    path = cutter_result.project_path / "frontend" / file_path
    assert path.is_file()


@pytest.mark.parametrize("file_path", CI_FILES)
def test_ci_files_generated(cutter_result, file_path: str):
    """Check that GitHub Actions were generated."""
    assert (cutter_result.project_path / ".github" / file_path).is_file()


def test_frontend_release_settings(cutter_result):
    """Keep releases attached to the generated monorepo."""
    path = cutter_result.project_path / "frontend/packages/volto-plone/.release-it.json"
    settings = json.loads(path.read_text())
    assert settings["github"]["release"] is False
    assert settings["npm"]["publish"] is False
    assert settings["plonePrePublish"]["publish"] is False


def test_repoplone_settings(cutter_result):
    """Describe the Nick and Volto workspaces in repository.toml."""
    path = cutter_result.project_path / "repository.toml"
    settings = tomli.loads(path.read_text())
    assert settings["backend"]["package"]["path"] == "backend"
    assert settings["backend"]["package"]["base_package"] == "@plone/nick"
    assert settings["frontend"]["package"]["path"] == ("frontend/packages/volto-plone")
    assert settings["frontend"]["package"]["base_package"] == "@plone/volto"


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        ["backend/package.json", "package"],
        ["backend/tsconfig.json", "tsconfig"],
        ["frontend/package.json", "package"],
        ["frontend/packages/volto-plone/package.json", "package"],
        [".github/workflows/backend.yml", "github-workflow"],
        [".github/workflows/changelog.yml", "github-workflow"],
        [".github/workflows/config.yml", "github-workflow"],
        [".github/workflows/frontend.yml", "github-workflow"],
        [".github/workflows/main.yml", "github-workflow"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)


def test_upstream_nick_configuration(cutter_result):
    """Generated configuration should use the current Plone Nick package."""
    project_path = cutter_result.project_path

    package_json = (project_path / "backend/package.json").read_text()
    assert '"@plone/nick": "workspace:^"' in package_json
    assert "@robgietema/nick" not in package_json

    config = (project_path / "backend/config.ts").read_text()
    assert "database: 'nick'" in config
    assert "user: 'nick'" in config
    assert "password: 'nick'" in config
    assert "'@plone/nick:core'" in config
    assert "'plone:default'" in config

    tsconfig = (project_path / "backend/tsconfig.json").read_text()
    assert '"@plone/nick": ["develop/nick/src"]' in tsconfig

    assert not (project_path / "backend/jsconfig.json").exists()
    assert not (project_path / "backend/eslint.config.mjs").exists()

    frontend_package = json.loads(
        (project_path / "frontend/package.json").read_text()
    )
    frontend_test = frontend_package["scripts"]["test"]
    assert frontend_test.count("--passWithNoTests") == 1

    frontend_makefile = (project_path / "frontend/Makefile").read_text()
    assert "CI=1 pnpm run test --passWithNoTests" not in frontend_makefile


def test_no_devops_scaffold(cutter_result):
    """Keep deployment and other monorepo extras out of this template."""
    project_path = cutter_result.project_path
    assert not (project_path / "devops").exists()
    assert not (project_path / "docker-compose.yml").exists()
