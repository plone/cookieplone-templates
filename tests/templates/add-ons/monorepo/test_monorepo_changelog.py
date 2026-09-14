"""Test Generator: changelog / towncrier setup."""

from pathlib import Path

import pytest

from tests.templates import CHANGELOG_TEMPLATE_NAME, TOWNCRIER_TYPES, expected_settings

REPOSITORY_URL = "https://github.com/collective/collective-addon"
# A monorepo add-on ships three independent towncrier setups: the
# repository itself, the backend package and the frontend add-on.

TOWNCRIER_CONFIGS = [
    "towncrier.toml",
    "backend/pyproject.toml",
    "frontend/packages/volto-addon/towncrier.toml",
]

NEWS_FOLDERS = [
    "news",
    "backend/news",
    "frontend/packages/volto-addon/news",
]

EXPECTED_SETTINGS = expected_settings(REPOSITORY_URL)


@pytest.mark.parametrize("folder", NEWS_FOLDERS)
def test_news_folder_has_changelog_template(cutter_result, folder: str):
    """Test the towncrier template is shipped inside the codebase."""
    path = cutter_result.project_path / folder / CHANGELOG_TEMPLATE_NAME
    assert path.is_file()


@pytest.mark.parametrize("folder", NEWS_FOLDERS)
def test_news_folder_has_gitkeep(cutter_result, folder: str):
    """Test the news folder is kept under version control."""
    path = cutter_result.project_path / folder / ".gitkeep"
    assert path.is_file()


@pytest.mark.parametrize("folder", NEWS_FOLDERS)
def test_changelog_template_is_not_rendered(cutter_result, folder: str):
    """Test the towncrier template is copied verbatim.

    The template uses Jinja syntax meant for towncrier, so the generator must
    not render it -- it has to be listed under ``config.no_render``.
    """
    path = cutter_result.project_path / folder / CHANGELOG_TEMPLATE_NAME
    content = path.read_text()
    assert '{% if sections[""] %}' in content
    assert "{{ definitions[category]['name'] }}" in content


@pytest.mark.parametrize("filename", TOWNCRIER_CONFIGS)
def test_towncrier_config_exists(cutter_result, towncrier_config, filename: str):
    """Test each codebase has a towncrier configuration."""
    path = cutter_result.project_path / filename
    assert path.is_file()
    assert towncrier_config(path) != {}


@pytest.mark.parametrize("filename", TOWNCRIER_CONFIGS)
@pytest.mark.parametrize("key,expected", list(EXPECTED_SETTINGS.items()))
def test_towncrier_settings(
    cutter_result, towncrier_config, filename: str, key: str, expected
):
    """Test towncrier settings match the ones shared by every codebase."""
    path = cutter_result.project_path / filename
    assert towncrier_config(path)[key] == expected


@pytest.mark.parametrize("filename", TOWNCRIER_CONFIGS)
def test_towncrier_types(cutter_result, towncrier_types, filename: str):
    """Test the news fragment types match the ones shared by every codebase."""
    path = cutter_result.project_path / filename
    assert towncrier_types(path) == TOWNCRIER_TYPES


@pytest.mark.parametrize("filename", TOWNCRIER_CONFIGS)
def test_towncrier_template_is_local(cutter_result, towncrier_config, filename: str):
    """Test towncrier points to the template shipped inside the codebase."""
    path = cutter_result.project_path / filename
    template = towncrier_config(path)["template"]
    assert template.endswith(f"news/{CHANGELOG_TEMPLATE_NAME}")
    assert "node_modules" not in template


@pytest.mark.parametrize("filename", TOWNCRIER_CONFIGS)
def test_towncrier_template_resolves(cutter_result, towncrier_config, filename: str):
    """Test the configured template path resolves to a generated file."""
    path = cutter_result.project_path / filename
    template = towncrier_config(path)["template"]
    resolved: Path = (path.parent / template).resolve()
    assert resolved.is_file()
