"""Test Generator: /frontend."""

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
    "package.json",
    "pnpm-workspace.yaml",
    "README.md",
    "volto.config.js",
]


@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_frontend_files(cutter_result, filename: str):
    """Test @plone/volto generator files exist."""
    frontend_folder = cutter_result.project_path / "frontend"
    path = frontend_folder / filename
    assert path.is_file()
