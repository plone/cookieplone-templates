import json

NON_EMBEDDED_NICK_TEMPLATES = ("volto_nick", "aurora_nick")


def test_nick_projects_use_shared_backend_source(templates_folder):
    """Non-embedded Nick projects should generate one shared backend scaffold."""
    for template_name in NON_EMBEDDED_NICK_TEMPLATES:
        template_path = templates_folder / "projects" / template_name
        config = json.loads((template_path / "cookieplone.json").read_text())
        subtemplate_ids = {
            item["id"] for item in config["config"]["subtemplates"]
        }

        assert "sub/nick_backend" in subtemplate_ids
        inline_backend = (
            template_path / "{{ cookiecutter.__folder_name }}" / "backend"
        )
        assert not any(path.is_file() for path in inline_backend.rglob("*"))


def test_shared_nick_backend_contains_scaffold(templates_folder):
    """Keep the backend implementation in its dedicated subtemplate."""
    backend = (
        templates_folder
        / "sub"
        / "nick_backend"
        / "{{ cookiecutter.__folder_name }}"
    )

    assert (backend / "package.json").is_file()
    assert (backend / "config.ts").is_file()
    assert (backend / "src/profiles/default/metadata.json").is_file()


def test_shared_nick_backend_selects_frontend_profile(templates_folder):
    """Keep frontend-specific root content in the shared backend source."""
    root_profile = (
        templates_folder
        / "sub"
        / "nick_backend"
        / "{{ cookiecutter.__folder_name }}"
        / "src/profiles/default/documents/_root.json"
    ).read_text()

    assert 'cookiecutter.nick_frontend == "aurora"' in root_profile
    assert "Welcome to Plone Aurora!" in root_profile
    assert "Welcome to Nick!" in root_profile
