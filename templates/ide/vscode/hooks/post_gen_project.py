from collections import OrderedDict
from pathlib import Path

from cookieplone.utils import post_gen

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}

REPLACEMENTS = (
    ("}./", "}/"),
    (".//", "./"),
    ("../", "./"),
    ("//", "/"),
    ("{workspaceFolder}backend", "{workspaceFolder}/backend"),
    ("{workspaceFolder}frontend", "{workspaceFolder}/frontend"),
    (".frontend", "./frontend"),
)


def handle_path_cleanup(context: OrderedDict, output_dir: Path):
    """Cleanup path in JSON files."""
    files = output_dir.glob("**/*.json")
    for file in files:
        content = file.read_text()
        for old, new in REPLACEMENTS:
            content = content.replace(old, new)
        file.write_text(content)


def action_handlers(context: OrderedDict) -> list[post_gen.PostGenAction]:
    """Return action handlers."""
    actions: list[post_gen.PostGenAction] = [
        {
            "handler": handle_path_cleanup,
            "title": "Fix paths in the generated files",
            "enabled": True,
        },
    ]
    return actions


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    # Action handlers
    post_gen.run_post_gen_actions(context, output_dir, action_handlers(context))


if __name__ == "__main__":
    main()
