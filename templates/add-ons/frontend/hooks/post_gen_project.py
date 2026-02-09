"""Post generation hook."""

import os
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console, files

context: OrderedDict = {{cookiecutter}}

DOCUMENTATION_STARTER_REMOVE = [
    ".github",
    ".git",
]

TEMPLATES_FOLDER = "templates"


def remove_conditional_files(context, output_dir):
    if context["__test_framework"] == "jest":
        (
            output_dir
            / "packages"
            / context["frontend_addon_name"]
            / "vitest.config.mjs"
        ).unlink()
    else:
        (output_dir / "jest-addon.config.js").unlink()

    if context["volto_version"] < "19":
        (output_dir / ".pnpmfile.cjs").unlink()


def generate_docs_starter(context, output_dir):
    """Generate documentation scaffold"""

    folder_name = "docs"
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/docs/starter",
        output_dir,
        "docs",
        context,
        DOCUMENTATION_STARTER_REMOVE,
    )
    files.remove_files(output_dir / folder_name, DOCUMENTATION_STARTER_REMOVE)


def generate_ci_gh_frontend_addon(context, output_dir):
    """Generate GitHub CI."""

    ci_context = OrderedDict({
        "npm_package_name": context["__npm_package_name"],
        "node_version": context["__node_version"],
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ci/gh_frontend_addon",
        output_dir,
        ".github",
        ci_context,
    )


def generate_ide_vscode(context, output_dir):
    """Generate VS Code configuration."""

    vscode_context = OrderedDict({
        "backend_path": "",
        "frontend_path": "/",
        "ansible_path": "",
        "__cookieplone_repository_path": context["__cookieplone_repository_path"],
    })
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ide/vscode", output_dir, ".vscode", vscode_context
    )


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

    remove_conditional_files(context, output_dir)

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
