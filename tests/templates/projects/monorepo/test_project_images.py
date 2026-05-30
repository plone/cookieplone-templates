import pytest


@pytest.mark.parametrize(
    "registry,expected_prefix,expected_separator",
    [
        ("github", "ghcr.io/plonegovbr/plone.org.br-", "-"),
        ("gitlab", "registry.gitlab.com/plonegovbr/plone.org.br/", "/"),
        ("docker_hub", "plonegovbr/plone.org.br-", "-"),
    ],
)
def test_image_prefix_registry(
    cookies, template_path, context, registry, expected_prefix, expected_separator
):
    """Test image prefix for different registries."""
    context["container_registry"] = registry
    result = cookies.bake(extra_context=context, template=template_path)

    assert result.exception is None
    assert result.exit_code == 0
    assert result.context["__container_registry_prefix_separator"] == expected_separator
    assert result.context["__container_image_prefix"] == expected_prefix

    # Check repository.toml
    repository_toml = result.project_path / "repository.toml"
    assert (
        f'container_images_prefix = "{expected_prefix}"' in repository_toml.read_text()
    )

    # Check Makefile in backend (from sub/project_settings)
    backend_makefile = result.project_path / "backend" / "Makefile"
    assert (
        "IMAGE_NAME_PREFIX := $(shell echo '$(REPOSITORY_SETTINGS)' | jq -r '.container_images_prefix')"
        in backend_makefile.read_text()
    )
    # Ensure no redundant dash
    assert "$(IMAGE_NAME_PREFIX)backend" in backend_makefile.read_text()
    assert "$(IMAGE_NAME_PREFIX)-backend" not in backend_makefile.read_text()
