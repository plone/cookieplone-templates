"""Post generation hook."""

from copy import deepcopy
from collections import OrderedDict
from pathlib import Path

from cookieplone.utils import console, files, git


context: OrderedDict = {{cookiecutter}}


# PATH OF CONTENT TO BE REMOVED
FEATURES_TO_REMOVE = {
    "feature_headless": [
        "serializers",
    ]
}

def handle_feature_headless(context: OrderedDict, output_dir: Path):
    package_namespace = context.get("__package_namespace")
    package_name = context.get("__package_name")
    output_dir = output_dir / "src" / package_namespace / package_name
    files.remove_files(output_dir, FEATURES_TO_REMOVE["feature_headless"])


def handle_git_initialization(context: OrderedDict, output_dir: Path):
    """Initialize a GIT repository for the project codebase."""
    git.initialize_repository(output_dir)


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    remove_headless = not int(context.get("feature_headless"))
    initialize_git = bool(int(context.get("__backend_addon_git_initialize")))
    # Cleanup / Git
    actions = [
        [
            handle_feature_headless,
            "Remove files used in headless setup",
            remove_headless,
        ],
        [
            handle_git_initialization,
            "Initialize Git repository",
            initialize_git,
        ],
    ]
    for func, title, enabled in actions:
        if not int(enabled):
            continue
        new_context = deepcopy(context)
        console.print(f" -> {title}")
        func(new_context, output_dir)

    msg = """
        [bold blue]{{ cookiecutter.title }}[/bold blue]

        Now, enter the repository run the code formatter with:

        make format

        start coding, and push to your organization.

        Sorry for the convenience,
        The Plone Community.
    """
    console.panel(
        title="New addon was generated", subtitle="", msg=msg, url="https://plone.org/"
    )


if __name__ == "__main__":
    main()
