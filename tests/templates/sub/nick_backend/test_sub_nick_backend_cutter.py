"""Test standalone generation of the shared Nick backend scaffold."""

import pytest


def test_creation(cookies, template_path, context: dict):
    """Generated backend should match the provided project slug."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == "project-title"
    assert result.project_path.is_dir()


@pytest.mark.parametrize(
    "file_path",
    [
        "config.ts",
        "package.json",
        "src/events/index.ts",
        "src/profiles/default/documents/_root.json",
        "src/profiles/default/metadata.json",
    ],
)
def test_backend_files_generated(cutter_result, file_path: str):
    """Generate the core Nick backend files."""
    path = cutter_result.project_path / file_path
    assert path.is_file()


def test_nick_configuration(cutter_result):
    """Use the current Nick defaults in standalone generation."""
    project_path = cutter_result.project_path

    config = (project_path / "config.ts").read_text()
    assert "database: 'nick'" in config
    assert "user: 'nick'" in config
    assert "password: 'nick'" in config

    root_profile = (
        project_path / "src/profiles/default/documents/_root.json"
    ).read_text()
    assert root_profile.startswith("{")
    assert "Welcome to Plone Volto with Plone Nick!" in root_profile
    assert "Welcome to Plone Aurora!" not in root_profile
    assert "{%" not in root_profile
