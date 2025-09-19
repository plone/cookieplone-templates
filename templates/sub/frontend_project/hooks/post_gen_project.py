"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console, files

context: OrderedDict = {{cookiecutter}}


LOCAL_FILES_FOLDER_NAME = "_project_files"


TO_REMOVE = [".github", "packages/volto-addon"]


def generate_addon(context, output_dir):
    """Run volto generator."""
    folder_name = output_dir.name
    output_dir = output_dir.parent
    context["frontend_addon_name"] = "volto-addon"
    context["initialize_documentation"] = "0"
    generator.generate_subtemplate(
        "../../add-ons/frontend", output_dir, folder_name, context, TO_REMOVE
    )


def cleanup(context, output_dir):
    """Remove references to volto-addon."""
    project_files_folder = output_dir / LOCAL_FILES_FOLDER_NAME
    project_files: list[Path] = list(project_files_folder.glob("*"))
    filenames = [path.name for path in project_files]
    # Remove old files
    files.remove_files(output_dir, filenames)
    for path in project_files:
        name = path.name
        path.rename(output_dir / name)
    # Remove templates folder
    files.remove_files(output_dir, [LOCAL_FILES_FOLDER_NAME])


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    # Setup frontend
    generate_addon(context, output_dir)
    # Cleanup
    cleanup(context, output_dir)
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
