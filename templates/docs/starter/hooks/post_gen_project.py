from collections import OrderedDict
from pathlib import Path

from cookieplone.utils import console, post_gen

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}


def action_handlers(context: OrderedDict) -> list[post_gen.PostGenAction]:
    """Return action handlers."""
    initialize_git = bool(int(context.get("initialize_git")))
    documentation_format = bool(int(context.get("__documentation_starter_format")))
    actions: list[post_gen.PostGenAction] = [
        {
            "handler": post_gen.run_make_format(),
            "title": "Format code",
            "enabled": documentation_format,
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

        Now, enter the docs folder, start documenting the code, and push to your organization.

        Sorry for the convenience,
        The Plone Community.
    """
    console.panel(
        title="New documentation scaffold was generated",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
