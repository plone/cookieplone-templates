"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path

from cookieplone.utils import post_gen
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}

POST_GEN_TO_REMOVE = {
    "cache": [
        "workflows/varnish.yml",
    ],
    "deploy": [
        "workflows/manual_deploy.yml",
    ],
    "docs": [
        "workflows/docs.yml",
        "workflows/rtd-pr-preview.yml",
    ],
    "classic": [
        "workflows/frontend.yml",
    ],
}


SUBTEMPLATE_HANDLERS = {}


def action_handlers(context: OrderedDict) -> list[post_gen.PostGenAction]:
    """Return action handlers."""
    feature_headless = bool(context.get("feature_headless", True))
    actions: list[post_gen.PostGenAction] = [
        {
            "handler": post_gen.remove_files_by_key(POST_GEN_TO_REMOVE, "docs"),
            "title": "Remove unneeded documentation files",
            "enabled": not int(context.get("has_docs", "0")),
        },
        {
            "handler": post_gen.remove_files_by_key(POST_GEN_TO_REMOVE, "cache"),
            "title": "Remove unneeded cache files",
            "enabled": not int(context.get("has_cache", "0")),
        },
        {
            "handler": post_gen.remove_files_by_key(POST_GEN_TO_REMOVE, "deploy"),
            "title": "Remove unneeded deploy files",
            "enabled": not int(context.get("has_deploy", "0")),
        },
        {
            "handler": post_gen.remove_files_by_key(POST_GEN_TO_REMOVE, "classic"),
            "title": "Remove frontend files for Classic UI",
            "enabled": not feature_headless,
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
