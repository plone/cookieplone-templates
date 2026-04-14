"""Post generation hook."""

import json
from collections import OrderedDict
from pathlib import Path

from binaryornot.check import is_binary
from cookieplone import generator
from cookieplone.utils import console, npm, plone, post_gen
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}


BACKEND_ADDON_REMOVE: list[str] = [
    ".git",
]

DOCUMENTATION_STARTER_REMOVE: list[str] = [
    ".github",
    ".git",
]

FRONTEND_ADDON_REMOVE: list[str] = []


POST_GEN_TO_REMOVE: dict[str, list[str]] = {
    "devops-ansible": [
        "devops/.env_dist",
        "devops/.gitignore",
        "devops/ansible.cfg",
        "devops/etc",
        "devops/inventory",
        "devops/Makefile",
        "devops/playbooks",
        "devops/requirements",
        "devops/tasks",
        "devops/README.md",
    ],
    "devops-gha": [
        "devops/.env_gha",
        "devops/README-GHA.md",
    ],
    "docs": [
        "docs/LICENSE.md",
        "docs/.git",
        "docs/.github",
    ],
}

TEMPLATES_FOLDER: str = "templates"


def _fix_frontend_addon_name(context: OrderedDict) -> OrderedDict:
    """Fix frontend_addon_name if it is a scoped package."""
    frontend_addon_name: str = context["frontend_addon_name"]
    if frontend_addon_name.startswith("@") and "/" in frontend_addon_name:
        npm_package_name = frontend_addon_name
        frontend_addon_name = npm.unscoped_package_name(npm_package_name)
        context["npm_package_name"] = npm_package_name
        context["frontend_addon_name"] = frontend_addon_name
    return context


def _find_replace_in_folder(folder: Path, replacements: dict[str, str]):
    """Find and replace in all text files in a folder."""
    for file_path in folder.rglob("*"):
        if not file_path.is_file() or is_binary(str(file_path)):
            continue
        content = file_path.read_text()
        for find, replace in replacements.items():
            content = content.replace(find, replace)
        file_path.write_text(content)


def handle_backend_cleanup(context: OrderedDict, output_dir: Path):
    """Create namespace packages for the backend."""
    python_package_name: str = context["python_package_name"]
    plone.create_namespace_packages(
        output_dir / "backend/src/packagename", python_package_name, style="native"
    )


def generate_addons_backend(context: OrderedDict, output_dir: Path) -> Path:
    """Run Plone Addon generator."""
    folder_name = "backend"
    # Headless
    context["feature_headless"] = True
    context["initialize_ci"] = False
    context["initialize_documentation"] = False
    path = generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/add-ons/backend",
        output_dir,
        folder_name,
        context,
        BACKEND_ADDON_REMOVE,
        global_versions=versions,
    )
    return path


def generate_addons_frontend(context: OrderedDict, output_dir: Path) -> Path:
    """Run volto generator."""
    folder_name = "frontend"
    # Handle packages inside an organization
    context = _fix_frontend_addon_name(context)
    frontend_addon_name = context["frontend_addon_name"]
    context["initialize_documentation"] = False
    context["initialize_ci"] = False
    path = generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/add-ons/frontend",
        output_dir,
        folder_name,
        context,
        FRONTEND_ADDON_REMOVE,
        global_versions=versions,
    )
    # Handle .release-it.json
    release_it_path = path / "packages" / frontend_addon_name / ".release-it.json"
    if release_it_path.is_file():
        data = json.loads(release_it_path.read_text())
        # Disable GitHub releases
        data["github"]["release"] = False
        # Disable plonePrePublish
        data["plonePrePublish"]["publish"] = False
        # Disable npm
        data["npm"]["publish"] = False
        # Update file
        release_it_path.write_text(json.dumps(data, indent=2))

    # Replace Repository URL in all files
    frontend_repo_path = (
        "{{ cookiecutter.github_organization }}/{{ cookiecutter.frontend_addon_name }}"
    )
    frontend_addon_repo_url = f"https://github.com/{frontend_repo_path}"
    frontend_addon_repo_git = f"git@github.com:{frontend_repo_path}"
    replacements = {
        frontend_addon_repo_url: "{{ cookiecutter.__repository_url }}",
        frontend_addon_repo_git: "{{ cookiecutter.__repository_git }}",
    }
    _find_replace_in_folder(path, replacements)
    return path


def generate_docs_starter(context: OrderedDict, output_dir: Path) -> Path:
    """Generate documentation scaffold."""
    folder_name = "docs"
    path = generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/docs/starter",
        output_dir,
        folder_name,
        context,
        DOCUMENTATION_STARTER_REMOVE,
        global_versions=versions,
    )
    return path


def generate_sub_cache(context: OrderedDict, output_dir: Path) -> Path:
    """Add cache structure."""
    # Use the same base folder
    folder_name = output_dir.name
    parent_dir = output_dir.parent
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/sub/cache",
        parent_dir,
        folder_name,
        context,
        global_versions=versions,
    )


def generate_sub_project_settings(context: OrderedDict, output_dir: Path) -> Path:
    """Configure language and other settings."""
    # Use the same base folder
    folder_name = output_dir.name
    parent_dir = output_dir.parent
    context = _fix_frontend_addon_name(context)
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/sub/project_settings",
        parent_dir,
        folder_name,
        context,
        global_versions=versions,
    )


def generate_ci_gh_project(context: OrderedDict, output_dir: Path) -> Path:
    """Generate GitHub CI."""
    ci_context = OrderedDict({
        "npm_package_name": context["__npm_package_name"],
        "python_version": versions["backend_python"],
        "node_version": context["__node_version"],
        "has_cache": "1" if context["devops_cache"] else "0",
        "has_docs": "1" if context["initialize_documentation"] else "0",
        "has_deploy": "1" if context["devops_gha_deploy"] else "0",
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ci/gh_project",
        output_dir,
        ".github",
        ci_context,
        global_versions=versions,
    )


def generate_ide_vscode(context: OrderedDict, output_dir: Path) -> Path:
    """Generate VS Code configuration."""
    ansible_path = "devops/ansible" if context.get("devops_ansible") else ""
    vscode_context = OrderedDict({
        "backend_path": "backend",
        "frontend_path": "frontend",
        "ansible_path": ansible_path,
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ide/vscode",
        output_dir,
        ".vscode",
        vscode_context,
        global_versions=versions,
    )


SUBTEMPLATE_HANDLERS = {
    "add-ons/backend": generate_addons_backend,
    "add-ons/frontend": generate_addons_frontend,
    "docs/starter": generate_docs_starter,
    "sub/cache": generate_sub_cache,
    "sub/project_settings": generate_sub_project_settings,
    "ci/gh_project": generate_ci_gh_project,
    "ide/vscode": generate_ide_vscode,
}


def action_handlers(context: OrderedDict) -> list[post_gen.PostGenAction]:
    """Return action handlers."""
    initialize_git = bool(
        int(context.get("__project_git_initialize", 1))
    )  # {{ cookiecutter.__project_git_initialize }}
    feature_devops_ansible = bool(
        context.get("devops_ansible", False)
    )  # {{ cookiecutter.devops_ansible }}
    feature_gha_deploy = bool(
        context.get("devops_gha_deploy", False)
    )  # {{ cookiecutter.devops_gha_deploy }}
    feature_documentation = bool(
        context.get("initialize_documentation", False)
    )  # {{ cookiecutter.initialize_documentation }}
    backend_format = bool(
        int(context.get("__backend_addon_format", 1))
    )  # {{ cookiecutter.__backend_addon_format }}
    actions: list[post_gen.PostGenAction] = [
        {
            "handler": handle_backend_cleanup,
            "title": "Backend final cleanup",
            "enabled": True,
        },
        {
            "handler": post_gen.run_make_format("format", "backend"),
            "title": "Format backend code",
            "enabled": backend_format,
        },
        {
            "handler": post_gen.remove_files_by_key(
                POST_GEN_TO_REMOVE, "devops-ansible"
            ),
            "title": "Remove Ansible files",
            "enabled": not feature_devops_ansible,
        },
        {
            "handler": post_gen.remove_files_by_key(POST_GEN_TO_REMOVE, "devops-gha"),
            "title": "Remove GitHub Actions deployment files",
            "enabled": not feature_gha_deploy,
        },
        {
            "handler": post_gen.move_files([
                ("docs/.readthedocs.yaml", ".readthedocs.yml")
            ]),
            "title": "Organize documentation files",
            "enabled": feature_documentation,
        },
        {
            "handler": post_gen.remove_files_by_key(POST_GEN_TO_REMOVE, "docs"),
            "title": "Remove unneeded documentation files",
            "enabled": feature_documentation,
        },
        {
            "handler": post_gen.initialize_git_repository,
            "title": "Initialize Git repository",
            "enabled": initialize_git,
        },
    ]
    return actions


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )

    # Action handlers
    post_gen.run_post_gen_actions(context, output_dir, action_handlers(context))

    msg = """
        [bold blue]{{ cookiecutter.title }}[/bold blue]

        Now, code it, create a git repository, push to your organization.

        Sorry for the convenience,
        The Plone Community.
    """
    console.panel(
        title="New project was generated",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
