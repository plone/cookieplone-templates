from pathlib import Path

import pytest
import tomli


@pytest.fixture(scope="module")
def template_repository_root(cookieplone_root, template_folder: str) -> Path:
    return cookieplone_root / "templates" / template_folder


@pytest.fixture(scope="module")
def template_path(template_repository_root) -> str:
    return str(template_repository_root)


@pytest.fixture
def build_files_list():
    def func(root_dir: Path) -> list[Path]:
        """Build a list containing absolute paths to the generated files."""
        return [path for path in Path(root_dir).glob("*") if path.is_file()]

    return func


@pytest.fixture(scope="module")
def cutter_result(template_path, cookies_module, context):
    """Cookiecutter result."""
    return cookies_module.bake(extra_context=context, template=template_path)


@pytest.fixture
def generated_paths(cutter_result, build_files_list):
    # Return a list of paths generated from the project path
    return build_files_list(cutter_result.project_path)


@pytest.fixture
def generated_path(request, generated_paths):
    # The fixture receives a single path as an indirect parameter
    return generated_paths


@pytest.fixture(scope="session")
def towncrier_config():
    """Return a helper to parse a towncrier configuration file.

    Works for standalone ``towncrier.toml`` files and for ``pyproject.toml``
    files, as both store the settings under the ``[tool.towncrier]`` table.

    :returns: Callable receiving the path to a configuration file and returning
        the ``[tool.towncrier]`` table, or an empty dict if not present.
    """

    def func(path: Path) -> dict:
        data = tomli.loads(Path(path).read_text())
        return data.get("tool", {}).get("towncrier", {})

    return func


@pytest.fixture(scope="session")
def towncrier_types(towncrier_config):
    """Return a helper to extract the news fragment types from a configuration.

    :returns: Callable receiving the path to a configuration file and returning
        a mapping of fragment directory to its display name.
    """

    def func(path: Path) -> dict[str, str]:
        config = towncrier_config(path)
        return {entry["directory"]: entry["name"] for entry in config.get("type", [])}

    return func
