"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone.utils import console

context: OrderedDict = {{cookiecutter}}


def handle_docs_instructions(context: OrderedDict, output_dir: Path) -> None:
    """Remove docs/instructions if not needed."""
    to_keep = context.get("docs_file")
    all_instructions = [
        path
        for path in output_dir.glob("*-docs.instructions.md")
        if path.name != to_keep
    ]
    for path in all_instructions:
        path.unlink()
    if to_keep:
        new_name = "docs.instructions.md"
        console.info(f"- Renaming {to_keep} as {new_name}.")
        path = output_dir / to_keep
        path.rename(output_dir / new_name)


def handle_volto(context: OrderedDict, output_dir: Path) -> None:
    """Remove volto if not needed."""
    if context.get("has_volto") != "1":
        path = output_dir / "volto.instructions.md"
        if path.exists():
            console.info("- Removing volto.instructions.md as not needed.")
            path.unlink()


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    handle_docs_instructions(context, output_dir)
    handle_volto(context, output_dir)


if __name__ == "__main__":
    main()
