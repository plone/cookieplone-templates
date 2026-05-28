import pytest


@pytest.mark.parametrize(
    "registry,expected_prefix,expected_separator",
    [
        ("github", "ghcr.io/collective/collective-addon-", "-"),
        ("gitlab", "registry.gitlab.com/collective/collective-addon/", "/"),
        ("docker_hub", "collective/collective-addon-", "-"),
    ],
)
def test_monorepo_addon_image_prefix_registry(
    cookies, template_path, context, registry, expected_prefix, expected_separator
):
    """Test image prefix for different registries in Monorepo Add-on template."""
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

    # Check root Makefile
    root_makefile = result.project_path / "Makefile"
    # In monorepo addon, acceptance images use IMAGE_NAME_PREFIX
    assert "$(IMAGE_NAME_PREFIX)frontend:acceptance" in root_makefile.read_text()
    assert "$(IMAGE_NAME_PREFIX)-frontend:acceptance" not in root_makefile.read_text()
