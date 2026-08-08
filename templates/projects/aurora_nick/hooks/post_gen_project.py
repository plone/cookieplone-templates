"""Post generation hook."""

import json
from collections import OrderedDict
from pathlib import Path

from binaryornot.check import is_binary
from cookieplone import generator
from cookieplone.utils import console, npm
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}

TEMPLATES_FOLDER = "templates"


def _find_replace_in_folder(folder: Path, replacements: dict[str, str]):
    """Find and replace strings in text files below a folder."""
    for file_path in folder.rglob("*"):
        if not file_path.is_file() or is_binary(str(file_path)):
            continue
        content = file_path.read_text()
        for find, replace in replacements.items():
            content = content.replace(find, replace)
        file_path.write_text(content)


def generate_addons_aurora(context: OrderedDict, output_dir: Path) -> Path:
    """Generate the Aurora workspace in the frontend folder."""
    frontend_context = context.copy()
    npm_package_name = frontend_context["frontend_addon_name"]
    frontend_addon_name = npm.unscoped_package_name(npm_package_name)
    frontend_context["frontend_addon_name"] = frontend_addon_name
    frontend_context["npm_package_name"] = npm_package_name
    frontend_context["__npm_package_name"] = npm_package_name
    frontend_context["__version_package"] = "1.0.0"
    path = generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/add-ons/aurora_addon",
        output_dir,
        "frontend",
        frontend_context,
        [".github", ".vscode"],
        global_versions=versions,
    )

    release_it_path = path / "packages" / frontend_addon_name / ".release-it.json"
    if release_it_path.is_file():
        data = json.loads(release_it_path.read_text())
        data["github"]["release"] = False
        data["npm"]["publish"] = False
        release_it_path.write_text(json.dumps(data, indent=2))

    frontend_repo_path = (
        "{{ cookiecutter.github_organization }}/"
        "{{ cookiecutter.frontend_addon_name }}"
    )
    replacements = {
        f"https://github.com/{frontend_repo_path}": "{{ cookiecutter.__repository_url }}",
        f"git@github.com:{frontend_repo_path}": "{{ cookiecutter.__repository_git }}",
    }
    _find_replace_in_folder(path, replacements)
    return path


def generate_ide_vscode(context: OrderedDict, output_dir: Path) -> Path:
    """Generate VS Code configuration for both workspaces."""
    vscode_context = OrderedDict(
        {
            "backend_path": "backend",
            "frontend_path": "frontend",
            "ansible_path": "",
            "__cookieplone_repository_path": context[
                "__cookieplone_repository_path"
            ],
        }
    )
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ide/vscode",
        output_dir,
        ".vscode",
        vscode_context,
        global_versions=versions,
    )


def generate_ci_gh_aurora_nick(context: OrderedDict, output_dir: Path) -> Path:
    """Generate GitHub Actions for the Nick and Aurora workspaces."""
    ci_context = OrderedDict(
        {
            "python_version": versions["backend_python"],
            "node_version": context["__node_version"],
            "frontend_package_name": context["__frontend_package_name"],
            "__cookieplone_repository_path": context[
                "__cookieplone_repository_path"
            ],
        }
    )
    return generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/ci/gh_aurora_nick",
        output_dir,
        ".github",
        ci_context,
        global_versions=versions,
    )


SUBTEMPLATE_HANDLERS = {
    "add-ons/aurora_addon": generate_addons_aurora,
    "ci/gh_aurora_nick": generate_ci_gh_aurora_nick,
    "ide/vscode": generate_ide_vscode,
}


def main():
    """Generate the frontend and finish the project."""
    output_dir = Path().cwd()

    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )

    msg = """
        [bold blue]{{ cookiecutter.project_slug }}[/bold blue]

        Next steps:

        cd {{ cookiecutter.project_slug }}
        make install

        Configure the PostgreSQL connection in `backend/config.ts`, then run:

        make backend-migrate
        make backend-seed

        Start the backend and frontend in separate terminals:

        make backend-start
        make frontend-start
    """
    console.panel(
        title=":tada: New project was generated :tada:",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
