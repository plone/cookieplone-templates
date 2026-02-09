"""Pytest configuration."""

import pytest


@pytest.fixture(scope="module")
def template_folder() -> str:
    return "ide/vscode"


@pytest.fixture(scope="session")
def context(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "backend_path": "/backend",
            "frontend_path": "/frontend",
            "ansible_path": "/devops/ansible",
        },
        cookieplone_root,
        "ide_vscode",
    )


@pytest.fixture(scope="session")
def context_frontend_addon(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "backend_path": "",
            "frontend_path": "/",
            "ansible_path": "",
        },
        cookieplone_root,
        "ide_vscode",
    )


@pytest.fixture(scope="session")
def context_backend_addon(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "backend_path": "/",
            "frontend_path": "",
            "ansible_path": "",
        },
        cookieplone_root,
        "ide_vscode",
    )


@pytest.fixture(scope="session")
def context_monorepo_addon(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "backend_path": "/backend",
            "frontend_path": "/frontend",
            "ansible_path": "",
        },
        cookieplone_root,
        "ide_vscode",
    )


@pytest.fixture(scope="session")
def context_classic_project(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context."""
    return annotate_context(
        {
            "backend_path": "/backend",
            "frontend_path": "",
            "ansible_path": "/devops/ansible",
        },
        cookieplone_root,
        "ide_vscode",
    )
