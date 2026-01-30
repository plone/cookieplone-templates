"""Post generation hook."""

from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from cookieplone.utils import console, files

context: OrderedDict = {{cookiecutter}}

POST_GEN_TO_REMOVE = {
    "cache-0": [
        "workflows/varnish.yml",
    ],
    "deploy-0": [
        "workflows/manual_deploy.yml",
    ],
    "docs-0": [
        "workflows/docs.yml",
        "workflows/rtd-pr-preview.yml",
    ],
}


def handle_docs_cleanup(context: OrderedDict, output_dir: Path):
    """Clean up GitHub Actions docs."""
    answer = context.get("has_docs")
    key = f"docs-{answer}"
    to_remove = POST_GEN_TO_REMOVE.get(key, [])
    files.remove_files(output_dir, to_remove)


def handle_cache_cleanup(context: OrderedDict, output_dir: Path):
    """Clean up GitHub Actions cache."""
    answer = context.get("has_cache")
    key = f"cache-{answer}"
    to_remove = POST_GEN_TO_REMOVE.get(key, [])
    files.remove_files(output_dir, to_remove)


def handle_deploy_cleanup(context: OrderedDict, output_dir: Path):
    """Clean up GitHub Actions deploy."""
    answer = context.get("has_deploy")
    key = f"deploy-{answer}"
    to_remove = POST_GEN_TO_REMOVE.get(key, [])
    files.remove_files(output_dir, to_remove)


def run_actions(actions: list, output_dir: Path):
    for func, title, enabled in actions:
        if not int(enabled):
            continue
        new_context = deepcopy(context)
        console.print(f" -> {title}")
        func(new_context, output_dir)


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    # Cleanup
    actions = [
        [handle_docs_cleanup, "Remove unneeded documentation files", "1"],
        [handle_cache_cleanup, "Remove unneeded cache files", "1"],
        [handle_deploy_cleanup, "Remove unneeded deploy files", "1"],
    ]
    run_actions(actions, output_dir)


if __name__ == "__main__":
    main()
