from collections import OrderedDict
from pathlib import Path
from random import choice
from string import ascii_letters, digits

from cookieplone.utils import console, post_gen

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}


def generate_vaultpass(context: OrderedDict, output_dir: Path):
    """Generate a vault password file for Ansible."""
    vault_pass_path = output_dir / ".vault_pass"
    value = "".join(choice(ascii_letters + digits) for _ in range(32))  # noQA: S311
    if not vault_pass_path.exists():
        vault_pass_path.write_text(value)
        console.print(f"Vault password file created at {vault_pass_path}")
    else:
        console.print(f"Vault password file already exists at {vault_pass_path}")


def action_handlers(context: OrderedDict) -> list[post_gen.PostGenAction]:
    """Return action handlers."""
    initialize_git = bool(int(context.get("initialize_git")))
    actions: list[post_gen.PostGenAction] = [
        {
            "handler": generate_vaultpass,
            "title": "Generate Ansible vault password",
            "enabled": True,
        },
        {
            "handler": post_gen.initialize_git_repository,
            "title": "Initialize Git repository",
            "enabled": initialize_git,
        },
    ]
    return actions


def main():
    """Final fixes."""
    output_dir = Path().cwd()

    # Action handlers
    post_gen.run_post_gen_actions(context, output_dir, action_handlers(context))

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
