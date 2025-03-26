"""Test cookiecutter generation with distribution feature enabled."""

import pytest


@pytest.fixture(scope="session")
def cutter_result(cookies_session, context_distribution):
    """Cookiecutter result."""
    return cookies_session.bake(extra_context=context_distribution)


def test_creation(cookies, context_distribution: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context_distribution)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context_distribution["python_package_name"]
    assert result.project_path.is_dir()


def test_variable_substitution(build_files_list, variable_pattern, cutter_result):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        for line in open(path):
            match = variable_pattern.search(line)
            msg = f"cookiecutter variable not replaced in {path}"
            assert match is None, msg


def test_trove_classifier_set(cutter_result):
    """Check feature-specific files were not generated."""
    trove_classifier = "Framework :: Plone :: Distribution"
    pyproject = cutter_result.project_path / "pyproject.toml"
    assert trove_classifier in pyproject.read_text()
