"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone.utils import post_gen

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}

POST_GEN_TO_REMOVE = {
    "unnecessary": [
        "backend/mx.ini",
        "backend/src/packagename/profiles/uninstall",
        "backend/tests/setup/test_setup_uninstall.py",
    ],
}


def action_handlers(context: OrderedDict) -> list[post_gen.PostGenAction]:
    """Return action handlers."""
    actions: list[post_gen.PostGenAction] = [
        {
            "handler": post_gen.remove_files_by_key(POST_GEN_TO_REMOVE, "unnecessary"),
            "title": "Remove unnecessary files",
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
