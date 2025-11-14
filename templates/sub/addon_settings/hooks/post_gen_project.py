"""Post generation hook."""

from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone.utils import console, files

context: OrderedDict = {{cookiecutter}}


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    actions = []
    for func, title, enabled in actions:
        if not int(enabled):
            continue
        new_context = deepcopy(context)
        console.print(f" -> {title}")
        func(new_context, output_dir)


if __name__ == "__main__":
    main()
