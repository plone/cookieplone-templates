"""Post generation hook."""

import json
import subprocess
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console, files, git, npm, plone

context: OrderedDict = {{cookiecutter}}


BACKEND_ADDON_REMOVE = [
    ".git",
]

DOCUMENTATION_STARTER_REMOVE = [
    ".github",
    ".git",
]

FRONTEND_ADDON_REMOVE = []


POST_GEN_TO_REMOVE = {
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
    "docs-1": ["docs/LICENSE.md"],
}

TEMPLATES_FOLDER = "templates"


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
    """Find and replace in all files in a folder."""
    for file_path in folder.rglob("*"):
        if file_path.is_file():
            content = file_path.read_text()
            for find, replace in replacements.items():
                content = content.replace(find, replace)
            file_path.write_text(content)


def handle_devops_ansible(context: OrderedDict, output_dir: Path):
    """Clean up ansible."""
    to_remove = POST_GEN_TO_REMOVE.get("devops-ansible", [])
    files.remove_files(output_dir, to_remove)


def handle_devops_gha_deploy(context: OrderedDict, output_dir: Path):
    """Clean up gha deploy."""
    to_remove = POST_GEN_TO_REMOVE.get("devops-gha", [])
    files.remove_files(output_dir, to_remove)


def handle_docs_cleanup(context: OrderedDict, output_dir: Path):
    """Clean up GitHub Actions deploy."""
    answer = context.get("initialize_documentation")
    key = f"docs-{answer}"
    to_remove = POST_GEN_TO_REMOVE.get(key, [])
    files.remove_files(output_dir, to_remove)


def handle_docs_setup(context: OrderedDict, output_dir: Path):
    """Move files from /docs to the root."""
    files_to_move = [
        ["docs/.readthedocs.yaml", ".readthedocs.yml"],
    ]
    for src_path, dst_path in files_to_move:
        src = output_dir / src_path
        src.rename(output_dir / dst_path)


def handle_git_initialization(context: OrderedDict, output_dir: Path):
    """Initialize a GIT repository for the project codebase."""
    git.initialize_repository(output_dir)


def generate_addons_backend(context, output_dir):
    """Run Plone Addon generator."""

    folder_name = "backend"
    # Headless
    context["feature_headless"] = "1"
    context["initialize_ci"] = "0"
    context["initialize_documentation"] = "0"
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/add-ons/backend",
        output_dir,
        folder_name,
        context,
        BACKEND_ADDON_REMOVE,
    )
    files.remove_files(output_dir / folder_name, BACKEND_ADDON_REMOVE)


def generate_addons_frontend(context, output_dir):
    """Run volto generator."""
    folder_name = "frontend"
    # Handle packages inside an organization
    context = _fix_frontend_addon_name(context)
    frontend_addon_name = context["frontend_addon_name"]
    context["initialize_documentation"] = "0"
    context["initialize_ci"] = "0"
    path = generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/add-ons/frontend",
        output_dir,
        folder_name,
        context,
        FRONTEND_ADDON_REMOVE,
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


def generate_docs_starter(context, output_dir):
    """Generate documentation scaffold"""

    folder_name = "docs"
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/docs/starter",
        output_dir,
        folder_name,
        context,
        DOCUMENTATION_STARTER_REMOVE,
    )
    files.remove_files(output_dir / folder_name, DOCUMENTATION_STARTER_REMOVE)


def generate_sub_cache(context: OrderedDict, output_dir: Path):
    """Add cache structure."""
    # Use the same base folder
    folder_name = output_dir.name
    output_dir = output_dir.parent
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/sub/cache", output_dir, folder_name, context
    )


def generate_sub_project_settings(context: OrderedDict, output_dir: Path):
    """Configure language and other settings."""
    # Use the same base folder
    folder_name = output_dir.name
    output_dir = output_dir.parent
    context = _fix_frontend_addon_name(context)
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/sub/project_settings", output_dir, folder_name, context
    )


def generate_ci_gh_project(context, output_dir):
    """Generate GitHub CI."""

    ci_context = OrderedDict({
        "npm_package_name": context["__npm_package_name"],
        "container_image_prefix": context["__container_image_prefix"],
        "python_version": context["__python_version"],
        "node_version": context["__node_version"],
        "has_cache": context["devops_cache"],
        "has_docs": context["initialize_documentation"],
        "has_deploy": context["devops_gha_deploy"],
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ci/gh_project",
        output_dir,
        ".github",
        ci_context,
    )


def generate_ide_vscode(context, output_dir):
    """Generate VS Code configuration."""

    ansible_path = "devops/ansible" if context.get("devops_ansible") == "1" else ""
    vscode_context = OrderedDict({
        "backend_path": "/backend",
        "frontend_path": "/frontend",
        "ansible_path": ansible_path,
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ide/vscode", output_dir, ".vscode", vscode_context
    )


def run_actions(actions: list, output_dir: Path):
    for func, title, enabled in actions:
        if not int(enabled):
            continue
        new_context = deepcopy(context)
        console.print(f" -> {title}")
        func(new_context, output_dir)


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    initialize_git = bool(
        int(context.get("__project_git_initialize"))
    )  # {{ cookiecutter.__project_git_initialize }}
    backend_format = bool(
        int(context.get("__backend_addon_format"))
    )  # {{ cookiecutter.__backend_addon_format }}

    subtemplates = context.get(
        "__cookieplone_subtemplates", []
    )  # {{ cookiecutter.__cookieplone_subtemplates }}
    funcs = {k: v for k, v in globals().items() if k.startswith("generate_")}
    for template_id, title, enabled in subtemplates:
        # Convert sub/cache -> generate_sub_cache
        template_slug = template_id.replace("/", "_").replace("-", "")
        func_name = f"generate_{template_slug}"
        func = funcs.get(func_name)
        if not func:
            raise ValueError(f"No handler available for sub_template {template_id}")
        elif not int(enabled):
            console.print(f" -> Ignoring ({title})")
            continue
        new_context = deepcopy(context)
        console.print(f" -> {title}")
        func(new_context, output_dir)

    # Create namespace packages
    plone.create_namespace_packages(
        output_dir / "backend/src/packagename",
        context.get("python_package_name"),
        style="native",
    )

    # Run format
    if backend_format:
        backend_folder = output_dir / "backend"
        # Run make format in the backend folder
        cmd = f"make -C {backend_folder} format"
        subprocess.call(cmd, shell=True)  # noQA: S602

    # Cleanup / Git
    actions = [
        [
            handle_devops_ansible,
            "Remove Ansible files",
            not int(context.get("devops_ansible")),  # {{ cookiecutter.devops_ansible }}
        ],
        [
            handle_devops_gha_deploy,
            "Remove GitHub Actions deployment files",
            not int(
                context.get("devops_gha_deploy")
            ),  # {{ cookiecutter.devops_gha_deploy }}
        ],
        [
            handle_docs_setup,
            "Organize documentation files",
            int(
                context.get("initialize_documentation")
            ),  # {{ cookiecutter.initialize_documentation }}
        ],
        [handle_docs_cleanup, "Remove unneeded documentation files", "1"],
        [
            handle_git_initialization,
            "Initialize Git repository",
            initialize_git,
        ],
    ]
    run_actions(actions, output_dir)

    # Do a second run add newly created files
    if initialize_git:
        repo = git.repo_from_path(output_dir)
        repo.git.add(output_dir)

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
