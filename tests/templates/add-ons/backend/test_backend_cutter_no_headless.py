"""Test cookiecutter generation without headless feature."""

import pytest


@pytest.fixture(scope="module")
def cutter_result(template_path, cookies_module, context_no_headless):
    """Cookiecutter result."""
    return cookies_module.bake(
        extra_context=context_no_headless, template=template_path
    )


def test_creation(cookies, template_path, context_no_headless: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context_no_headless, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context_no_headless["python_package_name"]
    assert result.project_path.is_dir()


def test_variable_substitution(build_files_list, variable_pattern, cutter_result):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        with open(path) as fh:
            for line in fh:
                match = {pattern.search(line) for pattern in variable_pattern}
                msg = f"cookiecutter variable not replaced in {path}"
                assert match == {None}, msg


def test_root_files_generated(cutter_result, root_file_path):
    """Check if root files were generated."""
    path = cutter_result.project_path / root_file_path
    assert path.exists()
    assert path.is_file()


def test_pkg_src_files_generated(cutter_result, pkg_file_path: str):
    """Check if distribution files were generated."""
    package_path = cutter_result.context["__package_path"]
    src_path = cutter_result.project_path / "src" / package_path
    path = src_path / pkg_file_path
    assert path.exists()
    assert path.is_file()


def test_pkg_src_headless_files_not_generated(
    cutter_result, pkg_file_path_headless: str
):
    """Check feature-specific files were not generated."""
    package_path = cutter_result.context["__package_path"]
    src_path = cutter_result.project_path / "src" / package_path
    path = src_path / pkg_file_path_headless
    assert path.exists() is False


GENERATED_FILES = [
    "browser/configure.zcml",
    "browser/overrides/.gitkeep",
    "browser/static/.gitkeep",
]


@pytest.mark.parametrize("file_path", GENERATED_FILES)
def test_created_files_for_classic(cutter_result, file_path: str):
    package_path = cutter_result.context["__package_path"]
    src_path = cutter_result.project_path / "src" / package_path
    path = src_path / file_path
    assert path.exists()
    assert path.is_file()
