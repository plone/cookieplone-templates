"""Test cookieplone generation for the Plone Aurora add-on."""

import json

import pytest
import yaml

GITHUB_ACTIONS = [
    ".github/workflows/acceptance.yml",
    ".github/workflows/changelog.yml",
    ".github/workflows/code.yml",
    ".github/workflows/i18n.yml",
    ".github/workflows/storybook.yml",
    ".github/workflows/unit.yml",
]

VSCODE_SETTINGS = [
    ".vscode/extensions.json",
    ".vscode/launch.json",
    ".vscode/settings.json",
]


ROOT_FILES = [
    *GITHUB_ACTIONS,
    *VSCODE_SETTINGS,
    ".storybook/main.js",
    ".storybook/preview.jsx",
    "app/entry.client.tsx",
    "app/entry.server.tsx",
    "app/root.tsx",
    "app/routes.ts",
    ".dockerignore",
    ".pnpmfile.cjs",
    "Dockerfile",
    "eslint.config.mjs",
    ".gitignore",
    ".npmignore",
    ".prettierignore",
    ".prettierrc",
    ".stylelintrc",
    "Makefile",
    "package.json",
    "pnpm-workspace.yaml",
    "public/favicon.ico",
    "README.md",
    "react-router.config.ts",
    "registry.config.ts",
    "server.js",
    "tsconfig.json",
    "vite.config.ts",
]

# The files of the core checkout, which the thin app doesn't need.
NOT_GENERATED = [
    "mrs.developer.json",
]


PKG_SRC_FILES = [
    ".gitignore",
    ".release-it.json",
    "CHANGELOG.md",
    "index.ts",
    "locales/de/LC_MESSAGES/volto.po",
    "locales/en/LC_MESSAGES/volto.po",
    "locales/es/LC_MESSAGES/volto.po",
    "locales/pt_BR/LC_MESSAGES/volto.po",
    "locales/volto.pot",
    "news/.gitkeep",
    "package.json",
    "public/.gitkeep",
    "towncrier.toml",
    "tsconfig.json",
    "types.d.ts",
    "vitest.config.ts",
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


@pytest.mark.parametrize("file_path", NOT_GENERATED)
def test_root_files_not_generated(cutter_result, file_path):
    """Check that the core checkout files are not generated."""
    assert not (cutter_result.project_path / file_path).exists()


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
        ["packages/seven-addon/package.json", "package"],
        ["packages/seven-addon/tsconfig.json", "tsconfig"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)


@pytest.mark.parametrize(
    "file_path,text,expected",
    [
        (
            ".github/workflows/changelog.yml",
            "uvx towncrier check --dir packages/",
            True,
        ),
        (".github/workflows/changelog.yml", "pipx", False),
        ("packages/seven-addon/.release-it.json", "uvx towncrier build", True),
        ("packages/seven-addon/.release-it.json", "pipx", False),
    ],
)
def test_content(cutter_result, file_path: str, text: str, expected: bool):
    path = (cutter_result.project_path / file_path).resolve()
    contents = path.read_text()
    assert (text in contents) is expected


def test_pnpm_configuration(cutter_result):
    """Use Aurora's pnpm version, and a catalog instead of the core checkout."""
    project_path = cutter_result.project_path
    package = json.loads((project_path / "package.json").read_text())
    workspace = yaml.safe_load((project_path / "pnpm-workspace.yaml").read_text())

    assert package["packageManager"] == "pnpm@12.14.0"
    assert "pnpm" not in package
    assert workspace["packages"] == [
        "packages/*",
        "packages/**/packages/*",
        "core/packages/*",
        "!core/packages/volto*",
    ]
    assert workspace["catalog"]["react-router"] == "8.5.0"
    assert workspace["catalog"]["@react-router/dev"] == "8.5.0"
    assert workspace["overrides"] == {
        "react": "^19.2.7",
        "react-dom": "^19.2.7",
        "jotai": "^2.12.5",
    }
    assert workspace["allowBuilds"]["@swc/core"] is True
    assert "cypress" not in workspace["allowBuilds"]
    assert not (project_path / ".npmrc").exists()

    addon = json.loads((project_path / "packages/seven-addon/package.json").read_text())
    assert addon["peerDependencies"]["i18next"] == "catalog:"
    for field in ("dependencies", "peerDependencies", "devDependencies"):
        for name, version in addon.get(field, {}).items():
            assert not version.startswith("workspace:"), name

    for workflow in GITHUB_ACTIONS:
        contents = (project_path / workflow).read_text()
        assert "npm install --global corepack@latest" in contents
        assert "corepack enable" in contents


def test_thin_app(cutter_result):
    """The repository is a React Router app that installs @plone/aurora."""
    project_path = cutter_result.project_path
    package = json.loads((project_path / "package.json").read_text())

    assert package["private"] is True
    assert package["type"] == "module"
    assert package["scripts"]["dev"] == "react-router dev"
    assert package["scripts"]["build"] == "react-router build"
    assert "workspace:*" in package["dependencies"].values()
    assert "REGISTRYCONFIG" not in json.dumps(package["scripts"])
    assert "@plone/aurora" not in json.dumps(package["scripts"])
    assert "ploneAurora()" in (project_path / "react-router.config.ts").read_text()
    assert "PloneAuroraVitePlugin()" in (project_path / "vite.config.ts").read_text()

    makefile = (project_path / "Makefile").read_text()
    assert "core/packages/registry/dist" not in makefile
    assert "build-deps" not in makefile
    assert "mrs-developer" not in makefile
    assert "./core/" not in (project_path / "eslint.config.mjs").read_text()


def test_core_overlay(cutter_result):
    """A Plone Aurora checkout in core/ replaces the released packages, opt-in."""
    project_path = cutter_result.project_path
    pnpmfile = (project_path / ".pnpmfile.cjs").read_text()
    assert "config.overrides[name] = 'workspace:*'" in pnpmfile
    assert "config.lockfile = false" in pnpmfile
    assert "if (!hasCore) return config;" in pnpmfile

    makefile = (project_path / "Makefile").read_text()
    assert "\ncore:" in makefile
    assert "\nbuild-core:" in makefile
    assert "\nremove-core:" in makefile
    install = makefile.split("\ninstall:")[1].split("\n\n")[0]
    assert "core" not in install

    assert "/core" in (project_path / ".gitignore").read_text().split()
    assert "core" in (project_path / ".dockerignore").read_text().split()
    assert "'core/'," in (project_path / "eslint.config.mjs").read_text()
    tsconfig = json.loads((project_path / "tsconfig.json").read_text())
    assert "core" in tsconfig["exclude"]


def test_aurora_version(cutter_result):
    """Depend on the resolved npm version of @plone/aurora."""
    project_path = cutter_result.project_path
    package = json.loads((project_path / "package.json").read_text())

    assert cutter_result.context["aurora_version"] == "1.0.0-alpha.5"
    assert package["dependencies"]["@plone/aurora"] == "1.0.0-alpha.5"
