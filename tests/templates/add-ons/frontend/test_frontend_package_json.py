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
        ("main", "src/index.ts"),
        ("devDependencies/'@plone/registry'", "workspace:*"),
        ("devDependencies/'@plone/types'", "workspace:*"),
        ("devDependencies/'@plone/scripts'", "workspace:*"),
    ],
)
def test_package_settings(traverse, cutter_result, load_config, path, expected):
    """Test /packages/<package_name>/package.json settings."""
    root_path = cutter_result.project_path
    package_path = root_path / "packages" / "volto-addon"
    config = load_config(package_path)
    result = traverse(config, path)
    assert result == expected


@pytest.fixture(scope="module")
def pinned_versions(cookieplone_root, load_json) -> dict:
    """Return the ``config.versions`` mapping from the repository config.

    :returns: Mapping of pin name to pinned value.
    """
    data = load_json(cookieplone_root / "cookieplone-config.json")
    return data["config"]["versions"]


@pytest.mark.parametrize(
    "package,key",
    [
        ("typescript", "frontend_typescript"),
        ("release-it", "frontend_release_it"),
    ],
)
def test_package_versions_from_config(
    traverse, cutter_result, load_config, pinned_versions, package, key
):
    """Test /packages/<package_name>/package.json uses the pinned versions.

    These are read from ``config.versions`` at render time, so a pin bumped in
    ``cookieplone-config.json`` must reach the generated add-on.
    """
    package_path = cutter_result.project_path / "packages" / "volto-addon"
    config = load_config(package_path)
    result = traverse(config, f"devDependencies/'{package}'")
    assert result == pinned_versions[key]


def test_root_mrs_developer_from_config(
    traverse, cutter_result, load_config, pinned_versions
):
    """Test /package.json uses the pinned mrs-developer version."""
    config = load_config(cutter_result.project_path)
    result = traverse(config, "devDependencies/'mrs-developer'")
    assert result == pinned_versions["frontend_mrs_developer"]


@pytest.mark.parametrize(
    "package,key",
    [
        ("@testing-library/react", "frontend_testing_library_react"),
        ("vitest", "frontend_vitest"),
    ],
)
def test_vitest_package_versions_from_config(
    traverse, cutter_result_volto_19, load_config, pinned_versions, package, key
):
    """Test the vitest branch of /packages/<package_name>/package.json.

    Volto 19 selects the vitest toolchain, which emits devDependencies that the
    jest branch used for Volto 18 never renders.
    """
    package_path = cutter_result_volto_19.project_path / "packages" / "volto-addon"
    config = load_config(package_path)
    result = traverse(config, f"devDependencies/'{package}'")
    assert result == pinned_versions[key]
