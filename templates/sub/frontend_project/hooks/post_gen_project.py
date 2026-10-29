"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import files
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}


LOCAL_FILES_FOLDER_NAME = "_project_files"

TEMPLATES_FOLDER: str = "templates"

TO_REMOVE = [".github", "packages/volto-addon"]


def generate_addons_frontend(context: OrderedDict, output_dir: Path) -> Path:
    """Run volto generator."""
    folder_name = output_dir.name
    output_dir = output_dir.parent
    context["frontend_addon_name"] = "volto-addon"
    context["initialize_documentation"] = False
    context["initialize_ci"] = False
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/add-ons/frontend",
        output_dir,
        folder_name,
        context,
        TO_REMOVE,
        global_versions=versions,
    )


SUBTEMPLATE_HANDLERS = {
    "add-ons/frontend": generate_addons_frontend,
}


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
    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )
    # Cleanup
    cleanup(context, output_dir)


if __name__ == "__main__":
    main()
