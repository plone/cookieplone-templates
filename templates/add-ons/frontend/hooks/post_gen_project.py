"""Post generation hook."""

import os
from copy import deepcopy
from pathlib import Path
from typing import OrderedDict

from cookieplone import generator
from cookieplone.utils import console, files

context: OrderedDict = {{cookiecutter}}

DOCUMENTATION_STARTER_REMOVE = [
    ".github",
    ".git",
]

TEMPLATES_FOLDER = "templates"


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


def main():
    """Final fixes."""

    output_dir = Path().cwd()
    subtemplates = context.get(
        "__cookieplone_subtemplates", []
    )  # {{ cookiecutter.__cookieplone_subtemplates }}
    funcs = {k: v for k, v in globals().items() if k.startswith("generate_")}
    for template_id, title, enabled in subtemplates:
        os.getenv("COOKIEPLONE_SUBTEMPLATE")
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
        [bold blue]{{ cookiecutter.frontend_addon_name }}[/bold blue]

        Now, enter the generated directory and finish the install:

        cd {{ cookiecutter.frontend_addon_name }}
        make install

        start coding, and push to your organization.

        Sorry for the convenience,
        The Plone Community.
    """
    console.panel(
        title=":tada: New addon was generated :tada:",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
