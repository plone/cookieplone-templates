import pytest


@pytest.fixture(scope="session")
def context_classic(annotate_context, cookieplone_root) -> dict:
    """Cookiecutter context for Classic UI."""
    return annotate_context(
        {
            "title": "Plone Classic Brasil",
            "project_slug": "classic.plone.org.br",
            "description": "Brazilian community website (Classic).",
            "hostname": "classic.plone.org.br",
            "author": "PloneGov-BR",
            "email": "gov@plone.org.br",
            "feature_headless": False,
            "use_prerelease_versions": "No",
            "plone_version": "6.0.10",
            "python_package_name": "plonegov.classic",
            "language_code": "en",
            "github_organization": "plonegovbr",
        },
        cookieplone_root,
        "project",
    )


@pytest.fixture(scope="module")
def cutter_result_classic(template_path, cookies_module, context_classic):
    """Cookiecutter result for Classic UI."""
    return cookies_module.bake(extra_context=context_classic, template=template_path)


def test_classic_generation(cutter_result_classic):
    assert cutter_result_classic.exit_code == 0
    assert cutter_result_classic.exception is None
    assert cutter_result_classic.project_path.exists()

    # Check that frontend folder does not exist
    frontend_dir = cutter_result_classic.project_path / "frontend"
    assert not frontend_dir.exists()

    # Check README.md
    readme = cutter_result_classic.project_path / "README.md"
    content = readme.read_text()
    assert "frontend" not in content.lower() or "headless" in content.lower()


def test_classic_context_variables(cutter_result_classic):
    """Check that even in classic mode, we have some safe defaults
    for frontend variables."""
    context = cutter_result_classic.context
    assert "volto_version" in context
    assert "__node_version" in context
    assert "frontend_addon_name" in context
    assert "__npm_package_name" in context
