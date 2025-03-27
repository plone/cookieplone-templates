from pathlib import Path

import pytest


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
