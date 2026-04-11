from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone.utils import console

context: OrderedDict = {{cookiecutter}}

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


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    # Cleanup / Git
    actions = [
        [
            handle_path_cleanup,
            "Fix paths in the generated files",
            True,
        ],
    ]
    for func, title, enabled in actions:
        if not int(enabled):
            continue
        new_context = deepcopy(context)
        console.print(f" -> {title}")
        func(new_context, output_dir)


if __name__ == "__main__":
    main()
