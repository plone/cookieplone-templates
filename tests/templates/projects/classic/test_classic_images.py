import pytest


@pytest.mark.parametrize(
    "registry,expected_prefix,expected_separator",
    [
        ("github", "ghcr.io/plonegovbr/plone.org.br-", "-"),
        ("gitlab", "registry.gitlab.com/plonegovbr/plone.org.br/", "/"),
        ("docker_hub", "plonegovbr/plone.org.br-", "-"),
    ],
)
def test_classic_image_prefix_registry(
    cookies, template_path, context, registry, expected_prefix, expected_separator
):
    """Test image prefix for different registries in Classic UI template."""
    context["container_registry"] = registry
    result = cookies.bake(extra_context=context, template=template_path)

    assert result.exception is None
    assert result.exit_code == 0
    assert result.context["__container_registry_prefix_separator"] == expected_separator
    assert result.context["__container_image_prefix"] == expected_prefix

    # Check backend Makefile (from sub/classic_project_settings)
    backend_makefile = result.project_path / "backend" / "Makefile"
    # Note: In classic template, the IMAGE_NAME_PREFIX is also set in backend/Makefile
    assert f"IMAGE_NAME_PREFIX={expected_prefix}" in backend_makefile.read_text()
    # Ensure no redundant dash
    assert "$(IMAGE_NAME_PREFIX)backend" in backend_makefile.read_text()
    assert "$(IMAGE_NAME_PREFIX)-backend" not in backend_makefile.read_text()
