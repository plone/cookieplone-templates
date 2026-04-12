"""Post generation hook."""

import subprocess
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console, files, git, plone
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

TEMPLATES_FOLDER: str = "templates"


def handle_devops_ansible(context: OrderedDict, output_dir: Path):
    """Clean up ansible."""
    files.remove_files(output_dir, POST_GEN_TO_REMOVE["devops-ansible"])


def handle_devops_gha_deploy(context: OrderedDict, output_dir: Path):
    """Clean up gha deploy."""
    files.remove_files(output_dir, POST_GEN_TO_REMOVE["devops-gha"])


def handle_docs_cleanup(context: OrderedDict, output_dir: Path):
    """Clean up docs files based on initialize_documentation."""
    answer = "1" if context.get("initialize_documentation") else "0"
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


def handle_backend_cleanup(context: OrderedDict, output_dir: Path):
    """Final pass on the backend codebase."""
    python_package_name: str = context["python_package_name"]
    plone.create_namespace_packages(
        output_dir / "backend/src/packagename", python_package_name, style="native"
    )

    backend_format = bool(
        int(context.get("__backend_addon_format", 1))
    )  # {{ cookiecutter.__backend_addon_format }}
    if backend_format:
        backend_folder = output_dir / "backend"
        cmd = f"make -C {backend_folder} format"
        subprocess.call(  # noQA: S602
            cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )


def generate_addons_backend(context: OrderedDict, output_dir: Path) -> Path:
    """Run Plone Addon generator."""
    folder_name = "backend"
    context["feature_headless"] = False
    context["initialize_ci"] = False
    context["initialize_documentation"] = False
    path = generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/add-ons/backend",
        output_dir,
        folder_name,
        context,
        BACKEND_ADDON_REMOVE,
    )
    files.remove_files(output_dir / folder_name, BACKEND_ADDON_REMOVE)
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
    )
    files.remove_files(output_dir / folder_name, DOCUMENTATION_STARTER_REMOVE)
    return path


def generate_sub_cache(context: OrderedDict, output_dir: Path) -> Path:
    """Add cache structure."""
    folder_name = output_dir.name
    parent_dir = output_dir.parent
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/sub/cache", parent_dir, folder_name, context
    )


def generate_sub_classic_project_settings(
    context: OrderedDict, output_dir: Path
) -> Path:
    """Configure language and other settings."""
    folder_name = output_dir.name
    parent_dir = output_dir.parent
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/sub/classic_project_settings",
        parent_dir,
        folder_name,
        context,
    )


def generate_ci_gh_classic_project(
    context: OrderedDict, output_dir: Path
) -> Path:
    """Generate GitHub CI."""
    ci_context = OrderedDict({
        "container_image_prefix": context["__container_image_prefix"],
        "python_version": versions["backend_python"],
        "has_cache": "1" if context["devops_cache"] else "0",
        "has_docs": "1" if context["initialize_documentation"] else "0",
        "has_deploy": "1" if context["devops_gha_deploy"] else "0",
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ci/gh_classic_project",
        output_dir,
        ".github",
        ci_context,
    )


def generate_ide_vscode(context: OrderedDict, output_dir: Path) -> Path:
    """Generate VS Code configuration."""
    ansible_path = "devops/ansible" if context.get("devops_ansible") else ""
    vscode_context = OrderedDict({
        "backend_path": "backend",
        "frontend_path": "",
        "ansible_path": ansible_path,
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ide/vscode", output_dir, ".vscode", vscode_context
    )


SUBTEMPLATE_HANDLERS = {
    "add-ons/backend": generate_addons_backend,
    "docs/starter": generate_docs_starter,
    "sub/cache": generate_sub_cache,
    "sub/classic_project_settings": generate_sub_classic_project_settings,
    "ci/gh_classic_project": generate_ci_gh_classic_project,
    "ide/vscode": generate_ide_vscode,
}


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

    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(context, output_dir, handlers=SUBTEMPLATE_HANDLERS)

    # Cleanup / Git
    actions = [
        [handle_backend_cleanup, "Backend final cleanup", True],
        [handle_devops_ansible, "Remove Ansible files", not feature_devops_ansible],
        [
            handle_devops_gha_deploy,
            "Remove GitHub Actions deployment files",
            not feature_gha_deploy,
        ],
        [handle_docs_setup, "Organize documentation files", feature_documentation],
        [handle_docs_cleanup, "Remove unneeded documentation files", "1"],
        [handle_git_initialization, "Initialize Git repository", initialize_git],
    ]
    run_actions(actions, output_dir)

    # Do a second run add newly created files
    if initialize_git:
        repo = git.repo_from_path(output_dir)
        if repo is not None:
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
