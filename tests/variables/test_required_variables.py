import pytest


@pytest.mark.parametrize(
    "key_name",
    ["__cookieplone_repository_path", "__cookieplone_template", "__folder_name"],
)
def test_template_has_required_keys(templates, key_name: str):
    for template_id, template_info in templates.items():
        config = template_info["config"]
        assert key_name in config, f"{template_id}: Does not have {key_name}"


def test_template_has_hooks(templates):
    for _, template_info in templates.items():
        hooks = template_info["hooks"]
        assert len(hooks.keys()) > 0
