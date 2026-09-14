"""Test Generator: changelog / towncrier setup."""

import pytest

from tests.templates import CHANGELOG_TEMPLATE_NAME, TOWNCRIER_TYPES, expected_settings

REPOSITORY_URL = "https://github.com/collective/project-title"

FRONTEND_CONFIG = "frontend/packages/volto-project-title/towncrier.toml"

TOWNCRIER_CONFIGS = [
    "backend/pyproject.toml",
    FRONTEND_CONFIG,
]


def _is_frontend_only(cutter_result, filename: str) -> bool:
    """Report if this configuration belongs to a codebase a Classic UI project lacks.

    :param cutter_result: Result of baking the template.
    :param filename: Path of the towncrier configuration, relative to the project.
    :returns: ``True`` when the project has no frontend and this is its config.
    """
    feature_headless = cutter_result.context.get("feature_headless", True)
    return not feature_headless and filename == FRONTEND_CONFIG


# This template is an overlay applied on top of an already generated codebase,
# so it ships the towncrier configuration but not the ``news`` folder itself --
# the template file is provided by the parent template.

EXPECTED_SETTINGS = expected_settings(REPOSITORY_URL)


@pytest.mark.parametrize("filename", TOWNCRIER_CONFIGS)
def test_towncrier_config_exists(cutter_result, towncrier_config, filename: str):
    """Test each codebase has a towncrier configuration."""
    path = cutter_result.project_path / filename
    if _is_frontend_only(cutter_result, filename):
        assert not path.exists()
        return
    assert path.is_file()
    assert towncrier_config(path) != {}


@pytest.mark.parametrize("filename", TOWNCRIER_CONFIGS)
@pytest.mark.parametrize("key,expected", list(EXPECTED_SETTINGS.items()))
def test_towncrier_settings(
    cutter_result, towncrier_config, filename: str, key: str, expected
):
    """Test towncrier settings match the ones shared by every codebase."""
    if _is_frontend_only(cutter_result, filename):
        pytest.skip("A Classic UI project has no frontend codebase.")
    path = cutter_result.project_path / filename
    assert towncrier_config(path)[key] == expected


@pytest.mark.parametrize("filename", TOWNCRIER_CONFIGS)
def test_towncrier_types(cutter_result, towncrier_types, filename: str):
    """Test the news fragment types match the ones shared by every codebase."""
    if _is_frontend_only(cutter_result, filename):
        pytest.skip("A Classic UI project has no frontend codebase.")
    path = cutter_result.project_path / filename
    assert towncrier_types(path) == TOWNCRIER_TYPES


@pytest.mark.parametrize("filename", TOWNCRIER_CONFIGS)
def test_towncrier_template_is_local(cutter_result, towncrier_config, filename: str):
    """Test towncrier points to the template shipped inside the codebase."""
    if _is_frontend_only(cutter_result, filename):
        pytest.skip("A Classic UI project has no frontend codebase.")
    path = cutter_result.project_path / filename
    template = towncrier_config(path)["template"]
    assert template.endswith(f"news/{CHANGELOG_TEMPLATE_NAME}")
    assert "node_modules" not in template
