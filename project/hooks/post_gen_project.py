"""Post generation hook."""

from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console, files, git, plone

context: OrderedDict = {{cookiecutter}}


BACKEND_ADDON_REMOVE = [
    ".github",
    ".git",
    ".meta.toml",
]

FRONTEND_ADDON_REMOVE = [".github"]

DEVOPS_TO_REMOVE = {
    "ansible": [
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
    "gha": [
        ".github/workflows/manual_deploy.yml",
        "devops/.env_gha",
        "devops/README-GHA.md",
    ],
}


def handle_devops_ansible(context: OrderedDict, output_dir: Path):
    """Clean up ansible."""
    files.remove_files(output_dir, DEVOPS_TO_REMOVE["ansible"])


def handle_devops_gha_deploy(context: OrderedDict, output_dir: Path):
    """Clean up ansible."""
    files.remove_files(output_dir, DEVOPS_TO_REMOVE["gha"])


def handle_git_initialization(context: OrderedDict, output_dir: Path):
    """Initialize a GIT repository for the project codebase."""
    git.initialize_repository(output_dir)


def generate_backend_addon(context, output_dir):
    """Run Plone Addon generator."""
    output_dir = output_dir
    folder_name = "backend"
    # Headless
    context["feature_headless"] = "1"
    generator.generate_subtemplate(
        "backend_addon", output_dir, folder_name, context, BACKEND_ADDON_REMOVE
    )
    files.remove_files(output_dir / folder_name, BACKEND_ADDON_REMOVE)


def generate_frontend_addon(context, output_dir):
    """Run volto generator."""
    generator.generate_subtemplate(
        "frontend_addon", output_dir, "frontend", context, FRONTEND_ADDON_REMOVE
    )


def generate_sub_cache(context: OrderedDict, output_dir: Path):
    """Add cache structure."""
    # Use the same base folder
    folder_name = output_dir.name
    output_dir = output_dir.parent
    generator.generate_subtemplate("sub/cache", output_dir, folder_name, context)


def generate_sub_project_settings(context: OrderedDict, output_dir: Path):
    """Configure language and other settings."""
    # Use the same base folder
    folder_name = output_dir.name
    output_dir = output_dir.parent
    generator.generate_subtemplate(
        "sub/project_settings", output_dir, folder_name, context
    )


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    initialize_git = bool(
        int(context.get("__project_git_initialize"))
    )  # {{ cookiecutter.__project_git_initialize }}
    backend_format = bool(
        int(context.get("__backend_addon_format"))
    )  # {{ cookiecutter.__backend_addon_format }}
    # Cleanup / Git
    actions = [
        [
            handle_devops_ansible,
            "Remove Ansible files",
            not int(context.get("devops_ansible")),  # {{ cookiecutter.devops_ansible }}
        ],
        [
            handle_devops_gha_deploy,
            "Remove GHA deployment files",
            not int(
                context.get("devops_gha_deploy")
            ),  # {{ cookiecutter.devops_gha_deploy }}
        ],
        [
            handle_git_initialization,
            "Initialize Git repository",
            initialize_git,
        ],
    ]
    for func, title, enabled in actions:
        if not int(enabled):
            continue
        new_context = deepcopy(context)
        console.print(f" -> {title}")
        func(new_context, output_dir)

    subtemplates = context.get(
        "__cookieplone_subtemplates", []
    )  # {{ cookiecutter.__cookieplone_subtemplates }}
    funcs = {k: v for k, v in globals().items() if k.startswith("generate_")}
    for template_id, title, enabled in subtemplates:
        # Convert sub/cache -> prepare_sub_cache
        func_name = f"generate_{template_id.replace('/', '_')}"
        func = funcs.get(func_name)
        if not func:
            raise ValueError(f"No handler available for sub_template {template_id}")
        elif not int(enabled):
            console.print(f" -> Ignoring ({title})")
            continue
        new_context = deepcopy(context)
        console.print(f" -> {title}")
        func(new_context, output_dir)

    # Run format
    if backend_format:
        backend_folder = output_dir / "backend"
        plone.format_python_codebase(backend_folder)

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
