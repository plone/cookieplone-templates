"""Test package.json template validation."""

from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def load_config(load_json):
    filename = "package.json"

    def func(path: Path) -> dict:
        path = path / filename
        return load_json(path)

    return func


@pytest.mark.parametrize(
    "path,expected",
    [
        ("name", "@plone-collective/volto-addon-dev"),
        ("version", "1.0.0-alpha.0"),
        ("dependencies/'@plone-collective/volto-addon'", "workspace:*"),
    ],
)
def test_frontend_root_settings(traverse, cutter_result, load_config, path, expected):
    """Test /package.json settings."""
    root_path = cutter_result.project_path
    config = load_config(root_path)
    result = traverse(config, path)
    assert result == expected


@pytest.mark.parametrize(
    "path,expected",
    [
        ("name", "@plone-collective/volto-addon"),
        ("version", "1.0.0-alpha.0"),
    ],
)
def test_package_settings(traverse, cutter_result, load_config, path, expected):
    """Test /packages/<package_name>/package.json settings."""
    root_path = cutter_result.project_path
    package_path = root_path / "packages" / "volto-addon"
    config = load_config(package_path)
    result = traverse(config, path)
    assert result == expected
