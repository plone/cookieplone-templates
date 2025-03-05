import os
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone.settings import QUIET_MODE_VAR
from cookieplone.utils import console, files, git, plone

context: OrderedDict = {{cookiecutter}}


def handle_format(context: OrderedDict, output_dir: Path):
    plone.format_python_codebase(output_dir)


def handle_git_initialization(context: OrderedDict, output_dir: Path):
    """Initialize a GIT repository for the project codebase."""
    git.initialize_repository(output_dir)


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    initialize_git = bool(
        int(context.get("__documentation_addon_git_initialize"))
    )  # {{ cookiecutter.__documentation_addon_git_initialize}}
    backend_format = bool(
        int(context.get("__documentation_addon_format"))
    )  # {{ cookiecutter.__documentation_addon_git_initialize}}
    # Cleanup / Git
    actions = [
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

    msg = """
        [bold blue]{{ cookiecutter.title }}[/bold blue]

        Now, enter the docs repository, start documenting the code, and push to your organization.

        Sorry for the convenience,
        The Plone Community.
    """
    console.panel(
        title="New documentation addon was generated",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
