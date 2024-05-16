import json
from pathlib import Path

import pytest

CONFIG_FILE = "cookiecutter.json"
VALID_HOOK_NAMES = [
    "pre_prompt.py",
    "pre_gen_project.py",
    "post_gen_project.py",
]


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
