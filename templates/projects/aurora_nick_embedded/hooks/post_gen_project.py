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

    vscode_context = OrderedDict({
        "backend_path": "",
        "frontend_path": "/",
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
    "ide/vscode": generate_ide_vscode,
}


def main():
    """Final fixes."""

    output_dir = Path().cwd()

    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )

    msg = """
        [bold blue]{{ cookiecutter.frontend_addon_name }}[/bold blue]

        Now, enter the generated directory and finish the install:

        cd {{ cookiecutter.frontend_addon_name }}
        make install

        Then, you need to populate the PostGreSQL database:
        - Configure the parameters of your connection to the database in the `registry.config.ts` file.
            ```
                connection: {
                    port: 5432,
                    host: 'your-database-host',
                    database: 'your-database-name',
                    user: 'your-username',
                    password: 'your-password',
                },
            ```
            Note: If you want to use the default configuration (eg. while developing), you can skip this step.
        - Run the command `pnpm nick:seed` to populate the database with the initial data and profile.

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
