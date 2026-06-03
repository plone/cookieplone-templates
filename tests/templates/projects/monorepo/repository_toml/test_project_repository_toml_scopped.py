"""Test repository.toml generation for a scoped frontend package name"""

from pathlib import Path
from typing import Any

import pytest
import tomli


@pytest.fixture
def repository_settings(cutter_result_scoped_frontend_package) -> dict:
    folder = cutter_result_scoped_frontend_package.project_path
    path: Path = folder / "repository.toml"
    return tomli.loads(path.read_text())


@pytest.mark.parametrize(
    "key,expected",
    [
        ["frontend.package.name", "@plone-collective/volto-ploneorgbr"],
        ["frontend.package.path", "frontend/packages/volto-ploneorgbr"],
        [
            "frontend.package.towncrier_settings",
            "frontend/packages/volto-ploneorgbr/towncrier.toml",
        ],
        [
            "frontend.package.changelog",
            "frontend/packages/volto-ploneorgbr/CHANGELOG.md",
        ],
    ],
)
def test_repository_toml_settings(repository_settings, key: str, expected: Any):
    """Test repository_toml settings."""
    value = repository_settings
    for key_ in key.split("."):
        value = value.get(key_, {})
    assert value == expected
