"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone.utils import console

context: OrderedDict = {{cookiecutter}}


def generate_agents_instructions(context: OrderedDict, output_dir: Path):
    """Add instructions structure."""
    from cookieplone import generator

    folder_name = "instructions"
    repository_path = context.get("__cookieplone_repository_path") or context.get(
        "_template"
    )
    new_ctx = OrderedDict({
        "has_volto": "1",
        "docs_file": "frontend-addon-docs.instructions.md",
        "__cookieplone_repository_path": repository_path,
    })
    generator.generate_subtemplate(
        "templates/agents/instructions", output_dir, folder_name, new_ctx
    )


def _generate_subtemplates(context: OrderedDict, output_dir: Path):
    """Generate subtemplates"""
    # Get selected subtemplates
    subtemplates = context.get(
        "__cookieplone_subtemplates", []
    )  # {{ cookiecutter.__cookieplone_subtemplates }}
    funcs = {k: v for k, v in globals().items() if k.startswith("generate_")}
    for template_id, title, enabled in subtemplates:
        template_slug = template_id.replace("/", "_").replace("-", "")
        func_name = f"generate_{template_slug}"
        func = funcs.get(func_name)
        if not func:
            raise ValueError(f"No handler available for sub_template {template_id}")
        elif not int(enabled):
            console.print(f" -> Ignoring ({title})")
            continue
        func(context, output_dir)


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    # Subtemplates
    _generate_subtemplates(context, output_dir)


if __name__ == "__main__":
    main()
