"""Test cookiecutter generation with all features enabled."""

import json

import pytest

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
    "src/config/settings.ts",
    "src/index.ts",
    "towncrier.toml",
    "tsconfig.json",
]


@pytest.mark.parametrize("file_path", PKG_SRC_FILES)
def test_pkg_src_files_generated(cutter_result, file_path: str):
    """Check if package files were generated."""
    package_name = cutter_result.context["__frontend_addon_name"]
    src_path = cutter_result.project_path / "frontend" / "packages" / package_name
    path = src_path / file_path
    assert path.exists()
    assert path.is_file()


def test_release_it_settings(cutter_result):
    """Test .release-it.json settings are correct."""
    frontend_folder = cutter_result.project_path / "frontend"
    filename = "packages/volto-addon/.release-it.json"
    path = frontend_folder / filename
    data = json.loads(path.read_text())
    assert data["github"]["release"] is False
    assert data["npm"]["publish"] is False
    assert data["plonePrePublish"]["publish"] is False
