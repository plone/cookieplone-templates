"""Post generation hook."""

import os
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone import generator
from cookieplone.settings import QUIET_MODE_VAR
from cookieplone.utils import console, files, git, plone

context: OrderedDict = {{cookiecutter}}


# PATH OF CONTENT TO BE REMOVED
FEATURES_TO_REMOVE = {
    "feature_headless": [
        "browser",
    ],
    "feature_classic": [
        "serializers",
    ],
}

DOCUMENTATION_STARTER_REMOVE = [
    ".github",
    ".git",
]

TEMPLATES_FOLDER = "templates"


def handle_feature_headless(context: OrderedDict, output_dir: Path):
    output_dir = output_dir / "src" / "packagename"
    files.remove_files(output_dir, FEATURES_TO_REMOVE["feature_headless"])


def handle_feature_classic(context: OrderedDict, output_dir: Path):
    output_dir = output_dir / "src" / "packagename"
    files.remove_files(output_dir, FEATURES_TO_REMOVE["feature_classic"])


def handle_create_namespace_packages(context: OrderedDict, output_dir: Path):
    plone.create_namespace_packages(
        output_dir / "src/packagename",
        context.get("python_package_name"),
        style="pkgutil",
    )


def generate_docs_starter(context, output_dir):
    """Generate documentation scaffold"""
    output_dir = output_dir
    folder_name = "docs"
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/docs/starter",
        output_dir,
        "docs",
        context,
        DOCUMENTATION_STARTER_REMOVE,
    )
    files.remove_files(output_dir / folder_name, DOCUMENTATION_STARTER_REMOVE)


def handle_format(context: OrderedDict, output_dir: Path):
    plone.format_python_codebase(output_dir)


def handle_git_initialization(context: OrderedDict, output_dir: Path):
    """Initialize a GIT repository for the project codebase."""
    git.initialize_repository(output_dir)


def main():
    """Final fixes."""
    output_dir = Path().cwd()
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
    # Cleanup / Git
    actions = [
        [
            handle_feature_headless,
            "Remove files used in classic UI setup",
            feature_headless,
        ],
        [
            handle_feature_classic,
            "Remove files used in classic UI setup",
            not feature_headless,
        ],
        [
            handle_create_namespace_packages,
            "Create namespace packages",
            create_namespace_packages,
        ],
        [
            handle_format,
            "Format code",
            backend_format,
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
