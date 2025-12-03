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
        ("name", "@plone-collective/volto-ploneorgbr-dev"),
        ("version", "1.0.0-alpha.0"),
        ("dependencies/'@plone-collective/volto-ploneorgbr'", "workspace:*"),
    ],
)
def test_frontend_root_settings(
    traverse, cutter_result_scoped_frontend_package, load_config, path, expected
):
    """Test /package.json settings."""
    root_path = cutter_result_scoped_frontend_package.project_path / "frontend"
    config = load_config(root_path)
    result = traverse(config, path)
    assert result == expected


@pytest.mark.parametrize(
    "path,expected",
    [
        ("name", "@plone-collective/volto-ploneorgbr"),
        ("version", "1.0.0-alpha.0"),
        ("main", "src/index.ts"),
        ("devDependencies/'@plone/registry'", "workspace:*"),
        ("devDependencies/'@plone/types'", "workspace:*"),
        ("devDependencies/'@plone/scripts'", "workspace:*"),
    ],
)
def test_package_settings(
    traverse, cutter_result_scoped_frontend_package, load_config, path, expected
):
    """Test /packages/<package_name>/package.json settings."""
    root_path = cutter_result_scoped_frontend_package.project_path
    package_path = root_path / "frontend" / "packages" / "volto-ploneorgbr"
    config = load_config(package_path)
    result = traverse(config, path)
    assert result == expected
