"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone.utils import console
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}


def generate_agents_instructions(context: OrderedDict, output_dir: Path):
    """Add instructions structure."""
    from cookieplone import generator

    folder_name = "instructions"
    repository_path = context.get("__cookieplone_repository_path") or context.get(
        "_template"
    )
    new_ctx = OrderedDict({
        "has_volto": "0",
        "docs_file": "backend-addon-docs.instructions.md",
        "__cookieplone_repository_path": repository_path,
    })
    generator.generate_subtemplate(
        "templates/agents/instructions",
        output_dir,
        folder_name,
        new_ctx,
        global_versions=versions,
    )


SUBTEMPLATE_HANDLERS = {
    "agents/instructions": generate_agents_instructions,
}


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )


if __name__ == "__main__":
    main()
