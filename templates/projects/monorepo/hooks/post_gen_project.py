"""Post generation hook."""

import json
import subprocess
from collections import OrderedDict
from copy import deepcopy
from datetime import date
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console, files, git, npm, plone

context: OrderedDict = {{cookiecutter}}

calver_date = f"{date.today().strftime('%Y%m%d')}.0"  # YYYYMMDD
configuration_version = f"{date.today().strftime('%Y%m%d')}001"  # YYYYMMDD

BACKEND_ADDON_REMOVE = [
    ".github",
    ".git",
]

DOCUMENTATION_STARTER_REMOVE = [
    ".github",
    ".git",
]

FRONTEND_ADDON_REMOVE = [".github"]


POST_GEN_TO_REMOVE = {
    "devops-gha": [
        ".github/workflows/manual_deploy.yml",
        "devops/.env_gha",
        "devops/README-GHA.md",
    ],
    "docs-0": [
        ".github/workflows/docs.yml",
        ".github/workflows/rtd-pr-preview.yml",
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


def handle_version(context: OrderedDict, output_dir: Path):
    """Update version.txt."""
    version_path = output_dir / "version.txt"
    version_path.write_text(calver_date)


def handle_devops_gha_deploy(context: OrderedDict, output_dir: Path):
    """Clean up gha deploy."""
    files.remove_files(output_dir, POST_GEN_TO_REMOVE["devops-gha"])


def handle_docs_cleanup(context: OrderedDict, output_dir: Path):
    """Clean up GitHub Actions deploy."""
    answer = context.get("initialize_documentation")
    key = f"docs-{answer}"
    files.remove_files(output_dir, POST_GEN_TO_REMOVE[key])


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
    output_dir = output_dir
    folder_name = "backend"
    context["initial_version"] = f"{calver_date}"
    context["configuration_version"] = f"{configuration_version}"
    # Headless
    context["feature_headless"] = "1"
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
    context["initial_version"] = f"{calver_date}.0"
    context["initialize_documentation"] = "0"
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


def generate_devops_ansible(context, output_dir):
    """Run Devops - Ansible generator."""
    output_dir = output_dir
    folder_name = "devops/ansible"

    context["stack_location"] = f"../stacks/{context['hostname']}.yml"
    context["stack_name"] = f"{context['__devops_stack_name']}"
    context["stack_prefix"] = f"{context['__devops_stack_prefix']}"
    context["hostname_or_ip"] = f"{context['hostname']}"

    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/devops/ansible",
        output_dir,
        folder_name,
        context,
        BACKEND_ADDON_REMOVE,
    )
    files.remove_files(output_dir / folder_name, BACKEND_ADDON_REMOVE)


def generate_docs_starter(context, output_dir):
    """Generate documentation scaffold"""
    output_dir = output_dir
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
    context["container_image_prefix"] = f"{context['__container_image_prefix']}"
    context["cookieplone_template"] = f"{context['__cookieplone_template']}"
    context["generator_sha"] = f"{context['__generator_sha']}"
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/sub/project_settings", output_dir, folder_name, context
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
        style="pkgutil",
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
            handle_version,
            "Update version.txt",
            True,
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
