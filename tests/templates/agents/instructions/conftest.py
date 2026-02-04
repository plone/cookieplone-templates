"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "agents/instructions"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "has_volto": "1",
            "docs": "frontend-addon-docs.instructions.md",
        },
        cookieplone_root,
        "agents_instructions",
    )


@pytest.fixture(scope="session")
def context_frontend_addon(context) -> dict:
    """Cookiecutter context."""
    return context


@pytest.fixture(scope="session")
def context_backend_addon(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "has_volto": "0",
            "docs": "backend-addon-docs.instructions.md",
        },
        cookieplone_root,
        "agents_instructions",
    )


@pytest.fixture(scope="session")
def context_monorepo_addon(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "has_volto": "1",
            "docs": "monorepo-addon-docs.instructions.md",
        },
        cookieplone_root,
        "agents_instructions",
    )


@pytest.fixture(scope="session")
def context_project(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "has_volto": "1",
            "docs": "project-docs.instructions.md",
        },
        cookieplone_root,
        "agents_instructions",
    )


@pytest.fixture(scope="session")
def context_classic_project(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "has_volto": "0",
            "docs": "project-clasic-docs.instructions.md",
        },
        cookieplone_root,
        "agents_instructions",
    )
