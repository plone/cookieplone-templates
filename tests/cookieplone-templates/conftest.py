from pathlib import Path

import pytest
from cookieplone import _types as t
from cookieplone.repository import get_template_options


@pytest.fixture(scope="session")
def all_templates(templates_folder) -> list[Path]:
    candidates = templates_folder.glob("**/cookiecutter.json")
    all_templates = []
    for candidate in candidates:
        parent = candidate.parent
        all_templates.append(parent)
    return all_templates


@pytest.fixture(scope="session")
def available_templates(
    cookieplone_root,
) -> dict[str, t.CookieploneTemplate]:
    # Get all templates, including hidden ones
    return get_template_options(cookieplone_root, True)


@pytest.fixture(scope="session")
def templates_by_path(
    available_templates,
) -> dict[Path, tuple[str, t.CookieploneTemplate]]:
    result = {v.path.resolve(): (k, v) for k, v in available_templates.items()}
    return result
