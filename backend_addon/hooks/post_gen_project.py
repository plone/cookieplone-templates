"""Post generation hook."""

import subprocess
import sys
from pathlib import Path

from cookieplone.utils import console, files

# PATH OF CONTENT TO BE REMOVED
TO_REMOVE_PATHS = {
    "feature_headless": [
        "serializers",
    ]
}


def run_cmd(command: str, shell: bool, cwd: str) -> bool:
    proc = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True)
    if proc.returncode:
        # Write errors to the main process stderr
        console.error(f"Error while running {command}")
    return False if proc.returncode else True


def remove_files(category: str):
    to_remove = TO_REMOVE_PATHS.get(category, [])
    package_namespace = "{{ cookiecutter.__package_namespace }}"
    package_name = "{{ cookiecutter.__package_name }}"
    base_path = Path("src") / package_namespace / package_name
    # Remove all files
    files.remove_files(base_path, to_remove)


def initialize_git():
    """Apply black and isort to the generated codebase."""
    console.info("Git repository")
    steps = [
        ["Initialize", ["git", "init", "."], False, "."],
        ["Add files", ["git", "add", "."], False, "."],
    ]
    for step in steps:
        msg, command, shell, cwd = step
        console.info(f" - {msg}")
        result = run_cmd(command, shell=shell, cwd=cwd)
        if not result:
            sys.exit(1)


def main():
    """Final fixes."""
    keep_headless = int("{{ cookiecutter.feature_headless }}")
    if not keep_headless:
        remove_files("feature_headless")
    initialize_git()
    msg = """
        [bold blue]{{ cookiecutter.title }}[/bold blue]

        Now, enter the repositorym run the code formatter with:

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
