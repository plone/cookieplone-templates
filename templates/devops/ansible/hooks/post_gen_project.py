from collections import OrderedDict
from copy import deepcopy
from pathlib import Path
from random import choice
from string import ascii_letters, digits

from cookieplone.utils import console, git

context: OrderedDict = {{cookiecutter}}


def generate_vaultpass(context: OrderedDict, output_dir: Path):
    """Generate a vault password file for Ansible."""
    vault_pass_path = output_dir / ".vault_pass"
    value = "".join(choice(ascii_letters + digits) for _ in range(32))  # noQA: S311
    if not vault_pass_path.exists():
        vault_pass_path.write_text(value)
        console.print(f"Vault password file created at {vault_pass_path}")
    else:
        console.print(f"Vault password file already exists at {vault_pass_path}")


def handle_git_initialization(context: OrderedDict, output_dir: Path):
    """Initialize a Git repository for the documentation codebase."""
    git.initialize_repository(output_dir)


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    initialize_git = bool(int(context.get("initialize_git")))
    # Cleanup / Git
    actions = [
        [
            generate_vaultpass,
            "Generate Ansible vault password",
            True,
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

        Now, enter the {{ cookiecutter.folder_name }} folder, start using your
        playbooks.

        Sorry for the convenience,
        The Plone Community.
    """
    console.panel(
        title="New Ansible setup created",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
