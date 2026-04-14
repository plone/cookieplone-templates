"""Post generation hook."""

import os
from collections import OrderedDict
from pathlib import Path

from cookieplone import generator
from cookieplone.settings import QUIET_MODE_VAR
from cookieplone.utils import console, files, plone, post_gen
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}


# PATH OF CONTENT TO BE REMOVED
POST_GEN_TO_REMOVE = {
    "feature_headless": [
        "src/packagename/browser",
    ],
    "feature_classic": [
        "src/packagename/serializers",
    ],
}

DOCUMENTATION_STARTER_REMOVE = [
    ".github",
    ".git",
]

TEMPLATES_FOLDER = "templates"


def handle_create_namespace_packages(context: OrderedDict, output_dir: Path):
    plone.create_namespace_packages(
        output_dir / "src/packagename",
        context.get("python_package_name"),
        style="native",
    )


def generate_ci_gh_backend_addon(context, output_dir):
    """Generate GitHub CI."""

    ci_context = OrderedDict({
        "plone_version": context["plone_version"],
        "python_version": context["__supported_versions_python"][-1],
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ci/gh_backend_addon",
        output_dir,
        ".github",
        ci_context,
        global_versions=versions,
    )


def generate_docs_starter(context, output_dir):
    """Generate documentation scaffold"""

    folder_name = "docs"
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/docs/starter",
        output_dir,
        folder_name,
        context,
        DOCUMENTATION_STARTER_REMOVE,
        global_versions=versions,
    )


def generate_ide_vscode(context, output_dir):
    """Generate VS Code configuration."""

    vscode_context = OrderedDict({
        "backend_path": "./",
        "frontend_path": "",
        "ansible_path": "",
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ide/vscode",
        output_dir,
        ".vscode",
        vscode_context,
        global_versions=versions,
    )


def handle_format(context: OrderedDict, output_dir: Path):
    plone.format_python_codebase(output_dir)


SUBTEMPLATE_HANDLERS = {
    "ci/gh_backend_addon": generate_ci_gh_backend_addon,
    "docs/starter": generate_docs_starter,
    "ide/vscode": generate_ide_vscode,
}


def action_handlers(context: OrderedDict) -> list[post_gen.PostGenAction]:
    """Return action handlers."""
    is_subtemplate = os.environ.get(QUIET_MODE_VAR) == "1"
    feature_headless = int(
        context.get("feature_headless")
    )  # {{ cookiecutter.__feature_headless }}
    create_namespace_packages = not is_subtemplate
    initialize_git = bool(
        int(context.get("__backend_addon_git_initialize"))
    )  # {{ cookiecutter.__backend_addon_git_initialize }}
    backend_format = bool(
        int(context.get("__backend_addon_format"))
    )  # {{ cookiecutter.__backend_addon_format }}
    actions: list[post_gen.PostGenAction] = [
        {
            "handler": post_gen.remove_files_by_key(
                POST_GEN_TO_REMOVE, "feature_headless"
            ),
            "title": "Remove files used in headless setup",
            "enabled": feature_headless,
        },
        {
            "handler": post_gen.remove_files_by_key(
                POST_GEN_TO_REMOVE, "feature_classic"
            ),
            "title": "Remove files used in classic UI setup",
            "enabled": not feature_headless,
        },
        {
            "handler": handle_create_namespace_packages,
            "title": "Create namespace packages",
            "enabled": create_namespace_packages,
        },
        {
            "handler": handle_format,
            "title": "Format code",
            "enabled": backend_format,
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

    # Action handlers
    post_gen.run_post_gen_actions(context, output_dir, action_handlers(context))

    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )

    msg = """
        [bold blue]{{ cookiecutter.title }}[/bold blue]

        Now, enter the repository, start coding, and push to your organization.

        Sorry for the convenience,
        The Plone Community.
    """
    console.panel(
        title="New addon was generated", subtitle="", msg=msg, url="https://plone.org/"
    )


if __name__ == "__main__":
    main()
