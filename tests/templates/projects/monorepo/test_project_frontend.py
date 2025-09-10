"""Test Generator: /frontend."""

import json

import pytest

EXPECTED_FILES = [
    ".dockerignore",
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
    "Dockerfile",
    "Makefile",
    "mrs.developer.json",
    "packages/volto-ploneorgbr/.release-it.json",
    "package.json",
    "pnpm-workspace.yaml",
    "README.md",
    "volto.config.js",
]


@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_frontend_files(cutter_result, filename: str):
    """Test frontend files exist."""
    frontend_folder = cutter_result.project_path / "frontend"
    path = frontend_folder / filename
    assert path.is_file()


def test_release_it_settings(cutter_result):
    """Test .release-it.json settings are correct."""
    frontend_folder = cutter_result.project_path / "frontend"
    filename = "packages/volto-ploneorgbr/.release-it.json"
    path = frontend_folder / filename
    data = json.loads(path.read_text())
    assert data["github"]["release"] is False
    assert data["npm"]["publish"] is False
    assert data["plonePrePublish"]["publish"] is False
