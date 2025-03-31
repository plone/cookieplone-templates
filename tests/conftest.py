import json
from pathlib import Path

import pytest
from pytest_cookies.plugin import Cookies

CONFIG_FILE = "cookiecutter.json"
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
        config = {}
        data = path / CONFIG_FILE
        if data.exists():
            config = json.loads(data.read_text())
        return config

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


@pytest.fixture(scope="module")
def cookies_module(request, tmpdir_factory, _cookiecutter_config_file):
    """Yield an instance of the Cookies helper class that can be used to
    generate a project from a template.

    Run cookiecutter:
        result = cookies.bake(extra_context={
            'variable1': 'value1',
            'variable2': 'value2',
        })
    """
    template_dir = request.config.option.template

    output_dir = tmpdir_factory.mktemp(f"cookies-{request.module.__name__}")
    output_factory = output_dir.mkdir

    yield Cookies(template_dir, output_factory, _cookiecutter_config_file)

    # Add option to keep generated output directories.
    if not request.config.option.keep_baked_projects:
        output_dir.remove()


@pytest.fixture
def volto_versions():
    versions = ["17.15.5", "16.31.4", "18.0.0-alpha.27"]
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
