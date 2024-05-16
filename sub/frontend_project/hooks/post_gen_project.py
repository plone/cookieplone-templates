"""Post generation hook."""

from collections import OrderedDict  # noQA
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console, files

context = {{cookiecutter}}


TO_REMOVE = [
    ".github",
    "packages/volto-addon"
]


def generate_addon(context, output_dir):
    """Run volto generator."""
    folder_name = output_dir.name
    output_dir = output_dir.parent
    context["frontend_addon_name"] = "volto-addon"
    generator.generate_subtemplate(
        "volto_addon", output_dir, folder_name, context, TO_REMOVE
    )

def cleanup(context, output_dir):
    """Remove references to volto-addon."""
    pass


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
