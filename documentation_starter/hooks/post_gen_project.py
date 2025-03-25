import os
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path
from textwrap import dedent

from cookieplone.utils import console
from cookieplone.utils import git
from cookieplone.utils import plone

output_path = Path().resolve()
context: OrderedDict = {{cookiecutter}}


def handle_format(context: OrderedDict, output_dir: Path):
    plone.format_python_codebase(output_dir)


def handle_git_initialization(context: OrderedDict, output_dir: Path):
    """Initialize a GIT repository for the documentation codebase."""
    git.initialize_repository(output_dir)


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    initialize_git = bool(int(context.get("initialize_git")))
    documentation_format = bool(int(context.get("__documentation_starter_format")))
    # Cleanup / Git
    actions = [
        [
            handle_format,
            "Format code",
            documentation_format,
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

    msg = dedent(
            f"""
            Project Title: [bold blue]{{ cookiecutter.title }}[/bold blue]

            - Output folder: [bold blue]{output_path}[/bold blue]

            Now, enter the docs folder at [bold blue]{{ cookiecutter.project_folder }}[/bold blue], start documenting the code, and push to your organization.

            1.  Build and serve the Docs:

                [bold blue]cd {output_path}
                make livehtml[/bold blue]

            2.  Watch the documentation live while you edit it.

                - [bold blue]Open your browser[/bold blue] at the url displayed in the console  
                - Default local url is: [bold blue]http://127.0.0.1:8050/[/bold blue]
                - Edit the documentation source and save.
                - Content is rebuild and updates in the browser live.

            Sorry for the convenience,
            The Plone Community.
    """
    )

    console.panel(
        title="New documentation scaffolding was generated",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
