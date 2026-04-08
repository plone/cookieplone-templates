import json
import re
from pathlib import Path
from typing import Any

import pytest

CONFIG_FILE_V1 = "cookiecutter.json"
CONFIG_FILE_V2 = "cookieplone.json"
VALID_HOOK_NAMES = [
    "pre_prompt.py",
    "pre_gen_project.py",
    "post_gen_project.py",
]


@pytest.fixture(scope="session")
def templates_folder() -> Path:
    tests_folder = Path(__file__).parent
    repo_folder = tests_folder.parent
    return repo_folder / "templates"


@pytest.fixture(scope="session")
def read_config():
    def func(path: Path) -> dict:
        v2 = path / CONFIG_FILE_V2
        if v2.exists():
            data = json.loads(v2.read_text())
            schema = data.get("schema", {})
            properties = schema.get("properties", {})
            # Flatten v2 schema to a {key: default} dict so tests that check for
            # presence of property names keep working with both formats.
            return {key: prop.get("default", "") for key, prop in properties.items()}
        v1 = path / CONFIG_FILE_V1
        if v1.exists():
            return json.loads(v1.read_text())
        return {}

    return func


@pytest.fixture(scope="session")
def get_hooks():
    def func(path: Path) -> dict:
        hooks = {}
        hook_files = (path / "hooks").glob("*.py")
        for hook_file in hook_files:
            if hook_file.name in VALID_HOOK_NAMES:
                hooks[hook_file.name] = hook_file
        return hooks

    return func


@pytest.fixture(scope="session")
def templates(read_config, get_hooks) -> list:
    templates = {}
    # Read top-level config
    cwd = Path().cwd().resolve()
    config = read_config(cwd)
    for template_id, info in config.get("templates", {}).items():
        path = (cwd / info["path"]).resolve()
        templates[template_id] = {
            "base_path": path,
            "config": read_config(path),
            "hooks": get_hooks(path),
        }
    return templates


@pytest.fixture(scope="session")
def cookieplone_root() -> dict:
    """Cookieplone root dir."""
    folder = Path(__file__).parent
    return folder.parent.resolve()



@pytest.fixture
def volto_versions():
    versions = ["18.10.0", "18.0.0-alpha.27", "17.15.5", "16.31.4"]
    return versions


@pytest.fixture
def plone_versions():
    versions = [
        "6.0.0",
        "6.0.0a1",
        "6.0.0a2",
        "6.0.0a3",
        "6.0.0a4",
        "6.0.0a5",
        "6.0.0a6",
        "6.0.0b1",
        "6.0.0b2",
        "6.0.0b3",
        "6.0.0rc1",
        "6.0.0rc2",
        "6.0.1",
        "6.0.10",
        "6.0.2",
        "6.0.3",
        "6.0.4",
        "6.0.5",
        "6.0.6",
        "6.0.7",
        "6.0.8",
        "6.0.9",
        "6.1.0a1",
        "6.1.0a2",
    ]
    return versions


@pytest.fixture(autouse=True)
def mock_npm_packages(monkeypatch, volto_versions):
    from cookieplone.utils import versions

    def get_npm_package_versions(*args, **kwargs):
        return volto_versions

    monkeypatch.setattr(versions, "get_npm_package_versions", get_npm_package_versions)


@pytest.fixture(autouse=True)
def mock_pypi_packages(monkeypatch, plone_versions):
    from cookieplone.utils import versions

    def get_pypi_package_versions(*args, **kwargs):
        return plone_versions

    monkeypatch.setattr(
        versions, "get_pypi_package_versions", get_pypi_package_versions
    )


@pytest.fixture(scope="session")
def load_json():
    def func(path: Path) -> dict | list:
        data = {}
        if path.exists():
            data = json.loads(path.read_text())
        return data

    return func


@pytest.fixture(scope="session")
def traverse():
    pattern = re.compile(r"'([^']+)'|([^/]+)")

    def func(data: dict | list, path: str) -> Any:
        func = None
        path_parts = path.split(":")
        if len(path_parts) == 2:
            func, path = path_parts
        else:
            path = path_parts[0]
        path_groups = pattern.findall(path)
        parts = [part[0] or part[1] for part in path_groups]
        value = data
        for part in parts:
            if isinstance(value, list):
                part = int(part)
            value = value[part]
        match func:
            # Add other functions here
            case "len":
                value = len(value)
            case "type":
                # This makes it easier to compare
                value = type(value).__name__
            case "is_uuid4":
                value = len(value) == 32 and value[15] == "4"
            case "keys":
                value = list(value.keys()) if isinstance(value, dict) else []
        return value

    return func
