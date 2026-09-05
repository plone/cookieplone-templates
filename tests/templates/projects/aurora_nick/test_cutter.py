"""Test cookiecutter generation for aurora_nick."""

import json

import pytest
import tomli
import yaml

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
    ".prettierrc",
    "Dockerfile",
    "Makefile",
    "README.md",
    "babel.config.json",
    "config.ts",
    "docker-compose.yml",
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
        "Dockerfile",
        "eslint.config.mjs",
        "Makefile",
        "package.json",
        "pnpm-workspace.yaml",
        "registry.config.ts",
        "packages/aurora-plone/package.json",
    ],
)
def test_frontend_files_generated(cutter_result, file_path: str):
    """Check if the Aurora frontend workspace was generated."""
    path = cutter_result.project_path / "frontend" / file_path
    assert path.is_file()


@pytest.mark.parametrize("file_path", CI_FILES)
def test_ci_files_generated(cutter_result, file_path: str):
    """Check that GitHub Actions were generated."""
    assert (cutter_result.project_path / ".github" / file_path).is_file()


def test_frontend_release_settings(cutter_result):
    """Keep releases attached to the generated monorepo."""
    path = (
        cutter_result.project_path / "frontend/packages/aurora-plone/.release-it.json"
    )
    settings = json.loads(path.read_text())
    assert settings["github"]["release"] is False
    assert settings["npm"]["publish"] is False


def test_repoplone_settings(cutter_result):
    """Describe the Nick and Aurora workspaces in repository.toml."""
    path = cutter_result.project_path / "repository.toml"
    settings = tomli.loads(path.read_text())
    assert settings["backend"]["package"]["path"] == "backend"
    assert settings["backend"]["package"]["base_package"] == "@plone/nick"
    assert settings["frontend"]["package"]["path"] == ("frontend/packages/aurora-plone")
    assert settings["frontend"]["package"]["base_package"] == "@plone/aurora"


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        ["backend/package.json", "package"],
        ["backend/tsconfig.json", "tsconfig"],
        ["frontend/package.json", "package"],
        ["frontend/packages/aurora-plone/package.json", "package"],
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
    assert "database: DB_NAME || 'nick'" in config
    assert "user: DB_USER || 'nick'" in config
    assert "password: DB_PASSWORD || 'nick'" in config
    assert "'@plone/nick:core'" in config
    assert "'plone:default'" in config

    tsconfig = (project_path / "backend/tsconfig.json").read_text()
    assert '"@plone/nick": ["develop/nick/src"]' in tsconfig

    assert not (project_path / "backend/jsconfig.json").exists()
    assert not (project_path / "backend/eslint.config.mjs").exists()


def test_aurora_frontend_configuration(cutter_result):
    """Generate Aurora from the Aurora add-on scaffold without its standalone CI."""
    project_path = cutter_result.project_path
    package_json = (project_path / "frontend/package.json").read_text()
    assert '"@plone/aurora": "workspace:*"' in package_json
    assert "@plone/aurora dev" in package_json
    assert (project_path / "frontend/registry.config.ts").is_file()
    server_config = (
        project_path / "frontend/packages/aurora-plone/config/server.ts"
    ).read_text()
    assert "process.env.PLONE_API_PATH || 'http://localhost:8080'" in server_config
    assert not (project_path / ".github/workflows/acceptance.yml").exists()

    mrs = json.loads((project_path / "frontend/mrs.developer.json").read_text())
    assert cutter_result.context["aurora_version"] == "1.0.0-alpha.5"
    assert mrs["core"]["tag"] == cutter_result.context["aurora_version"]
    assert "branch" not in mrs["core"]


def test_aurora_frontend_uses_pnpm_11(cutter_result):
    """Generate Aurora with its pnpm 11 workspace configuration."""
    frontend = cutter_result.project_path / "frontend"
    package = json.loads((frontend / "package.json").read_text())
    workspace = yaml.safe_load((frontend / "pnpm-workspace.yaml").read_text())

    assert package["packageManager"] == "pnpm@11.20.0"
    assert "pnpm" not in package
    assert workspace["overrides"]["jotai"] == "^2.12.5"
    assert workspace["allowBuilds"]["@tailwindcss/oxide"] is True
    assert "cypress" not in workspace["allowBuilds"]
    assert "*cypress*" not in workspace["publicHoistPattern"]
    assert "*playwright*" in workspace["publicHoistPattern"]
    assert not (frontend / ".npmrc").exists()

    addon = json.loads(
        (frontend / "packages/aurora-plone/package.json").read_text()
    )
    assert addon["peerDependencies"]["i18next"] == "catalog:"


def test_no_devops_scaffold(cutter_result):
    """Keep deployment and other monorepo extras out of this template."""
    project_path = cutter_result.project_path
    assert not (project_path / "devops").exists()
    assert not (project_path / "docker-compose.yml").exists()
