"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path
from cookieplone.utils import files

context: OrderedDict = {{cookiecutter}}

CLASSIC_TO_REMOVE = {
    "frontend",
}


def remove_frontend(output_dir):
    files.remove_files(output_dir, CLASSIC_TO_REMOVE)


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    if context["feature_headless"] == "0":
        remove_frontend(output_dir)


if __name__ == "__main__":
    main()
