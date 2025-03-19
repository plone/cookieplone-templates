"""Test Generator: /varnish (And Cache support)."""

import pytest

CACHE_FILES = [
    "backend/src/plonegov/ploneorgbr/profiles/default/registry/plone.cachepurging.interfaces.ICachePurgingSettings.xml",
    "backend/src/plonegov/ploneorgbr/profiles/default/registry/plone.caching.interfaces.ICacheSettings.xml",
    "devops/varnish/Dockerfile",
    "devops/varnish/etc/varnish.vcl",
]

GHA_ACTIONS_CI = [
    ".github/workflows/varnish.yml",
]


DEVOPS_FILES = CACHE_FILES + GHA_ACTIONS_CI


@pytest.mark.parametrize("filepath", DEVOPS_FILES)
def test_project_cache_files(cutter_devops_result_cache, filepath: str):
    """Test created files."""
    folder = cutter_devops_result_cache.project_path
    path = folder / filepath
    assert path.is_file()


@pytest.mark.parametrize("filepath", CACHE_FILES)
def test_project_no_cache(cutter_result_devops_no_cache, filepath: str):
    """Test Cache-related files are not present."""
    folder = cutter_result_devops_no_cache.project_path
    path = folder / filepath
    assert path.exists() is False


CACHE_CONFIGURATION = [
    [
        "backend/src/plonegov/ploneorgbr/profiles/default/metadata.xml",
        "plone.app.caching:default",
    ],
    [
        "backend/src/plonegov/ploneorgbr/profiles/default/metadata.xml",
        "plone.app.caching:with-caching-proxy",
    ],
    ["backend/src/plonegov/ploneorgbr/dependencies.zcml", "plone.app.caching"],
]


@pytest.mark.parametrize("filepath,content", CACHE_CONFIGURATION)
def test_project_no_cache_no_config(
    cutter_result_devops_no_cache, filepath: str, content: str
):
    """Test Cache-related configurations are not present."""
    folder = cutter_result_devops_no_cache.project_path
    file_content = (folder / filepath).read_text()
    assert content not in file_content


@pytest.mark.parametrize("filepath,content", CACHE_CONFIGURATION)
def test_project_no_cache_config(cutter_result, filepath: str, content: str):
    """Test Cache-related configurations are not present."""
    folder = cutter_result.project_path
    file_content = (folder / filepath).read_text()
    assert content in file_content
