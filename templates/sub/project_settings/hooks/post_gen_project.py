"""Post generation hook."""

from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone.utils import console, files

context: OrderedDict = {{cookiecutter}}


def handle_remove_files(context: OrderedDict, output_dir: Path):
    files_to_remove = [
        "backend/mx.ini",
        "backend/src/packagename/profiles/uninstall",
        "backend/tests/setup/test_setup_uninstall.py",
    ]
    output_dir = output_dir
    files.remove_files(output_dir, files_to_remove)


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    actions = [
        [
            handle_remove_files,
            "Remove unnecessary files",
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
