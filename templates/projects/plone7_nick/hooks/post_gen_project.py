"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}


TEMPLATES_FOLDER = "templates"


def generate_ide_vscode(context, output_dir):
    """Generate VS Code configuration."""
    vscode_context = OrderedDict(
        {
            "backend_path": "",
            "frontend_path": "/",
            "ansible_path": "",
            "__cookieplone_repository_path": context["__cookieplone_repository_path"],
        }
    )
    generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ide/vscode",
        output_dir,
        ".vscode",
        vscode_context,
        global_versions=versions,
    )


SUBTEMPLATE_HANDLERS = {
    "ide/vscode": generate_ide_vscode,
}


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )

    msg = """
        [bold blue]{{ cookiecutter.project_slug }}[/bold blue]

        Next steps:

        cd {{ cookiecutter.project_slug }}
        pnpm install

        Configure the PostgreSQL connection in `config.ts`, then run:

        pnpm migrate
        pnpm seed
        pnpm start
    """
    console.panel(
        title=":tada: New project was generated :tada:",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
