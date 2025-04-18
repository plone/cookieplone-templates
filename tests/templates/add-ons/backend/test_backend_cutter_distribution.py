"""Test cookiecutter generation with distribution feature enabled."""

import pytest


@pytest.fixture(scope="module")
def cutter_result(template_path, cookies_module, context_distribution):
    """Cookiecutter result."""
    return cookies_module.bake(
        extra_context=context_distribution, template=template_path
    )


def test_creation(cookies, template_path, context_distribution: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context_distribution, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context_distribution["python_package_name"]
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


def test_trove_classifier_set(cutter_result):
    """Check feature-specific files were not generated."""
    trove_classifier = "Framework :: Plone :: Distribution"
    pyproject = cutter_result.project_path / "pyproject.toml"
    assert trove_classifier in pyproject.read_text()
