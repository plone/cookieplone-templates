"""Post generation hook."""

import json
from collections import OrderedDict
from pathlib import Path

from cookieplone import generator
from cookieplone.utils import console
from cookieplone.utils.subtemplates import run_subtemplates

context: OrderedDict = {{cookiecutter}}
versions: dict | OrderedDict = {{versions}}

TEMPLATES_FOLDER = "templates"

NICK_SCRIPTS = {
    "nick:seed": (
        "REGISTRYCONFIG=$(pwd)/registry.config.ts "
        "pnpm --filter @robgietema/nick seed"
    ),
    "nick:seed:status": (
        "REGISTRYCONFIG=$(pwd)/registry.config.ts "
        "pnpm --filter @robgietema/nick seed:status"
    ),
    "nick:seed:upgrade": (
        "REGISTRYCONFIG=$(pwd)/registry.config.ts "
        "pnpm --filter @robgietema/nick seed:upgrade"
    ),
    "nick:migrate": (
        "REGISTRYCONFIG=$(pwd)/registry.config.ts "
        "pnpm --filter @robgietema/nick migrate"
    ),
    "nick:reset": (
        "REGISTRYCONFIG=$(pwd)/registry.config.ts "
        "pnpm --filter @robgietema/nick reset"
    ),
}


def _read_json(path: Path) -> dict:
    """Read a JSON file."""
    return json.loads(path.read_text())


def _write_json(path: Path, data: dict) -> None:
    """Write a consistently formatted JSON file."""
    path.write_text(f"{json.dumps(data, indent=2)}\n")


def _replace_once(path: Path, old: str, new: str) -> None:
    """Replace one expected scaffold fragment and fail on unexpected drift."""
    content = path.read_text()
    if content.count(old) != 1:
        msg = f"Expected exactly one occurrence of {old!r} in {path}"
        raise ValueError(msg)
    path.write_text(content.replace(old, new, 1))


def _add_nick_configuration(path: Path, context: OrderedDict) -> None:
    """Apply the Nick-specific changes to a generated Aurora add-on."""
    root_package_path = path / "package.json"
    root_package = _read_json(root_package_path)
    root_package["scripts"].update(NICK_SCRIPTS)
    root_package["dependencies"]["@robgietema/nick"] = "workspace:*"
    _write_json(root_package_path, root_package)

    mrs_developer_path = path / "mrs.developer.json"
    mrs_developer = _read_json(mrs_developer_path)
    mrs_developer["nick"] = {
        "output": "./",
        "package": "@robgietema/nick",
        "url": "git@github.com:robgietema/nick.git",
        "https": "https://github.com/robgietema/nick.git",
        "branch": "main",
        "filterBlobs": True,
    }
    _write_json(mrs_developer_path, mrs_developer)

    addon_package_path = (
        path / "packages" / context["frontend_addon_name"] / "package.json"
    )
    addon_package = _read_json(addon_package_path)
    addon_package["dependencies"]["@robgietema/nick"] = "workspace:*"
    _write_json(addon_package_path, addon_package)

    _replace_once(
        path / "pnpm-workspace.yaml",
        "  - 'core/apps/aurora'\n",
        "  - 'core/apps/aurora'\n  - 'nick'\n",
    )
    _replace_once(path / ".gitignore", "core\n", "core\n/nick\n")

    registry_config_path = path / "registry.config.ts"
    _replace_once(
        registry_config_path,
        "import { addons } from '@plone/aurora/registry.config';\n",
        "import path from 'node:path';\n"
        "import { addons } from '@plone/aurora/registry.config';\n"
        "import type { ConfigSettings } from '@robgietema/nick/src/types';\n",
    )
    _replace_once(
        registry_config_path,
        "addons.push",
        "const dirname = path.resolve(\n"
        "  process.env.REGISTRYCONFIG\n"
        "    ? path.dirname(process.env.REGISTRYCONFIG)\n"
        "    : process.cwd(),\n"
        ");\n\n"
        "export const nick: Partial<ConfigSettings> = {\n"
        "  blobs: 'db',\n"
        "  profiles: [\n"
        "    `${dirname}/nick/src/profiles/core`,\n"
        "    `${dirname}/packages/{{ cookiecutter.frontend_addon_name }}-nick/profiles/default`,\n"
        "  ],\n"
        "};\n\n"
        "addons.push",
    )


def generate_addons_aurora(context: OrderedDict, output_dir: Path) -> Path:
    """Generate the current Aurora add-on scaffold and add embedded Nick."""
    path = generator.generate_subtemplate(
        f"{TEMPLATES_FOLDER}/add-ons/aurora_addon",
        output_dir.parent,
        output_dir.name,
        context,
        [".vscode"],
        global_versions=versions,
    )
    _add_nick_configuration(path, context)
    return path


def generate_ide_vscode(context: OrderedDict, output_dir: Path) -> Path:
    """Generate VS Code configuration."""
    vscode_context = OrderedDict(
        {
            "backend_path": "",
            "frontend_path": "./",
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


SUBTEMPLATE_HANDLERS = {
    "add-ons/aurora_addon": generate_addons_aurora,
    "ide/vscode": generate_ide_vscode,
}


def main():
    """Generate Aurora, apply Nick integration, and finish the project."""
    output_dir = Path().cwd()

    # {{ cookiecutter.__cookieplone_subtemplates }}
    run_subtemplates(
        context, output_dir, handlers=SUBTEMPLATE_HANDLERS, global_versions=versions
    )

    msg = """
        [bold blue]{{ cookiecutter.frontend_addon_name }}[/bold blue]

        Next steps:

        cd {{ cookiecutter.frontend_addon_name }}
        make install

        Configure the PostgreSQL connection in `registry.config.ts`, then run:

        pnpm nick:migrate
        pnpm nick:seed

        Start Plone Aurora:

        make start
    """
    console.panel(
        title=":tada: New project was generated :tada:",
        subtitle="",
        msg=msg,
        url="https://plone.org/",
    )


if __name__ == "__main__":
    main()
