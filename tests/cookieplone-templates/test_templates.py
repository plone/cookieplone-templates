import pytest


def test_total_templates(all_templates):
    assert len(all_templates) == 9


def test_all_templates_should_be_listed(all_templates, templates_by_path):
    assert set(all_templates).difference(set(templates_by_path.keys())) == set()


@pytest.mark.parametrize(
    "template_id,title,hidden",
    [
        ("project", "Volto Project", False),
        ("classic_project", "Classic UI Project", False),
        ("backend_addon", "Backend Add-on for Plone", False),
        ("frontend_addon", "Frontend Add-on for Plone", False),
        (
            "documentation_starter",
            "Documentation scaffold for Plone projects",
            False
        ),
        ("sub/cache", "Cache settings for a monorepo Plone project", True),
        ("sub/frontend_project", "A frontend project (used in Container images)", True),
        (
            "sub/project_settings",
            "Project settings to be applied on top of a mono repo project",
            True,
        ),
        (
            "sub/classic_project_settings",
            "Project settings to be applied on top of a Classic UI project",
            True,
        ),
    ],
)
def test_template_settings(
    available_templates, template_id: str, title: str, hidden: bool
):
    assert template_id in available_templates
    template = available_templates[template_id]
    assert template.title == title
    assert template.hidden is hidden


def test_template_has_hooks(templates):
    for _, template_info in templates.items():
        hooks = template_info["hooks"]
        assert len(hooks.keys()) > 0
