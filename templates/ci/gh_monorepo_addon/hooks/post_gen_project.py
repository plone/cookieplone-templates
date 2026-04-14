"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone.utils import post_gen
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}

POST_GEN_TO_REMOVE = {
    "docs": [
        "workflows/docs.yml",
        "workflows/rtd-pr-preview.yml",
    ],
}


def generate_agents_instructions(context: OrderedDict, output_dir: Path):
    """Add instructions structure."""
    from cookieplone import generator

    folder_name = "instructions"
    repository_path = context.get("__cookieplone_repository_path") or context.get(
        "_template"
    )
    new_ctx = OrderedDict({
        "has_volto": "1",
        "docs_file": "monorepo-addon-docs.instructions.md",
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


def action_handlers(context: OrderedDict) -> list[post_gen.PostGenAction]:
    """Return action handlers."""
    actions: list[post_gen.PostGenAction] = [
        {
            "handler": post_gen.remove_files_by_key(POST_GEN_TO_REMOVE, "docs"),
            "title": "Remove unneeded documentation files",
            "enabled": not int(context.get("has_docs", "0")),
        },
    ]
    return actions


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )

    # Action handlers
    post_gen.run_post_gen_actions(context, output_dir, action_handlers(context))


if __name__ == "__main__":
    main()
