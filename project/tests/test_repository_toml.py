"""Test repository.toml generation"""

from pathlib import Path
from typing import Any

import pytest
import tomli


@pytest.fixture
def repository_settings(cutter_result) -> dict:
    folder = cutter_result.project_path
    path: Path = folder / "repository.toml"
    return tomli.loads(path.read_text())


@pytest.mark.parametrize(
    "key,expected",
    [
        ["repository.name", "plone.org.br"],
        ["repository.towncrier.section", "Project"],
        ["repository.towncrier.settings", "towncrier.toml"],
        ["backend.package.name", "plonegov.ploneorgbr"],
        ["backend.package.publish", False],
        ["backend.package.towncrier_settings", "backend/pyproject.toml"],
        ["backend.package.changelog", "backend/CHANGELOG.md"],
        ["frontend.package.name", "volto-ploneorgbr"],
        ["frontend.package.publish", False],
        [
            "frontend.package.towncrier_settings",
            "frontend/packages/volto-ploneorgbr/towncrier.toml",
        ],
        [
            "frontend.package.changelog",
            "frontend/packages/volto-ploneorgbr/CHANGELOG.md",
        ],
        ["cookieplone.template", "project"],
    ],
)
def test_repository_toml_settings(repository_settings, key: str, expected: Any):
    """Test repository_toml settings."""
    value = repository_settings
    for key_ in key.split("."):
        value = value.get(key_, {})
    assert value == expected


@pytest.mark.parametrize(
    "key",
    [
        "cookieplone.generated_date",
        "cookieplone.template_version",
    ],
)
def test_repository_toml_settings_not_empty(repository_settings, key: str):
    """Test repository_toml settings."""
    value = repository_settings
    for key_ in key.split("."):
        value = value.get(key_, {})
    assert value.strip()
