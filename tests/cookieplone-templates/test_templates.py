import pytest


def test_total_templates(all_templates):
    assert len(all_templates) == 21


def test_all_templates_should_be_listed(all_templates, templates_by_path):
    assert set(all_templates).difference(set(templates_by_path.keys())) == set()


@pytest.mark.parametrize(
    "template_id,title,hidden",
    [
        ("project", "Plone 6 Project", False),
        ("classic_project", "Plone 6 using Classic UI Project", False),
        (
            "plone7_nick_bff",
            "Plone 7 alpha using Nick as BFF",
            False,
        ),
        ("backend_addon", "Plone 6 Backend Add-on (Python)", False),
        ("frontend_addon", "Plone 6 Frontend Add-on", False),
        ("monorepo_addon", "Plone 6 Add-on (Frontend and Backend)", False),
        ("seven_addon", "Plone 7 alpha Frontend Add-on", False),
        ("documentation_starter", "Documentation scaffold for Plone projects", False),
        ("sub/cache", "Cache settings for a Plone 6 project", True),
        (
            "sub/frontend_project",
            "A Plone 6 frontend project (used in Container images)",
            True,
        ),
        (
            "sub/project_settings",
            "Project settings to be applied on top of a Plone 6 project",
            True,
        ),
        (
            "sub/addon_settings",
            "Add-on settings to be applied on top of a Plone 6 project.",
            True,
        ),
        (
            "sub/classic_project_settings",
            "Project settings to be applied on top of a Plone 6 using Classic UI project",
            True,
        ),
        (
            "devops_ansible",
            "Ansible Playbooks for Plone",
            True,
        ),
        (
            "ci_gh_backend_addon",
            "CI: GitHub Actions for Backend Add-on",
            True,
        ),
        (
            "ci_gh_frontend_addon",
            "CI: GitHub Actions for Frontend Add-on",
            True,
        ),
        (
            "ci_gh_monorepo_addon",
            "CI: GitHub Actions for Monorepo Add-on",
            True,
        ),
        (
            "ci_gh_project",
            "CI: GitHub Actions for Project",
            True,
        ),
        (
            "ci_gh_classic_project",
            "CI: GitHub Actions for a Plone 6 using Classic UI Project",
            True,
        ),
        (
            "agents_instructions",
            "Agents / LLM: Instructions",
            True,
        ),
        (
            "ide_vscode",
            "VSCode IDE Configuration",
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
