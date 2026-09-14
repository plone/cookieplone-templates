"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "ci/gh_aurora_nick"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "python_version": "3.14",
            "node_version": "24",
            "frontend_package_name": "aurora-plone",
        },
        cookieplone_root,
        "ci_gh_aurora_nick",
    )


@pytest.fixture(scope="session")
def bad_context() -> dict:
    """Cookiecutter context with invalid data."""
    return {"node_version": ""}


@pytest.fixture
def codebases() -> list[tuple[str, str]]:
    """Codebases checked by the changelog workflow."""
    return [
        ("frontend", "path-frontend"),
        ("repository", "path-root"),
    ]


@pytest.fixture
def guarded() -> bool:
    """Whether changelog checks use path filters."""
    return True


@pytest.fixture
def expects_python_version() -> bool:
    """Whether the changelog workflow pins Python."""
    return True
