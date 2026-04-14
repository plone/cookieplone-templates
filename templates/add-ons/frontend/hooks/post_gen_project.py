"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console, files
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}

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
        folder_name,
        context,
        DOCUMENTATION_STARTER_REMOVE,
        global_versions=versions,
    )


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
        global_versions=versions,
    )


def generate_ide_vscode(context, output_dir):
    """Generate VS Code configuration."""

    vscode_context = OrderedDict({
        "backend_path": "",
        "frontend_path": "./",
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


SUBTEMPLATE_HANDLERS = {
    "docs/starter": generate_docs_starter,
    "ci/gh_frontend_addon": generate_ci_gh_frontend_addon,
    "ide/vscode": generate_ide_vscode,
}


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )

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
