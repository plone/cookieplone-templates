"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "ci/gh_volto_nick"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "python_version": "3.14",
            "node_version": "24",
            "volto_version": "19.0.0",
            "image_name_prefix": "ghcr.io/collective/plone",
            "frontend_package_name": "volto-plone",
        },
        cookieplone_root,
        "ci_gh_volto_nick",
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
