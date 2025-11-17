"""Test volto.config.js template validation."""

from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def load_config():
    filename = "volto.config.js"

    def func(path: Path) -> str:
        path = path / filename
        return path.read_text()

    return func


@pytest.mark.parametrize(
    "string,expected",
    [
        ("const addons = ['volto-addon'];", False),
        ("const addons = ['@plone-collective/volto-addon'];", True),
    ],
)
def test_addon_set(cutter_result, load_config, string, expected):
    """Test the addon name is set on volto.config.js."""
    root_path = cutter_result.project_path
    config = load_config(root_path)
    assert (string in config) is expected


@pytest.mark.parametrize(
    "string,expected",
    [
        ("const addons = ['volto-addon'];", True),
        ("const addons = ['@plone-collective/volto-addon'];", False),
    ],
)
def test_addon_set_no_organization(
    cutter_result_no_organization, load_config, string, expected
):
    """Test the addon name is set on volto.config.js."""
    root_path = cutter_result_no_organization.project_path
    config = load_config(root_path)
    assert (string in config) is expected
