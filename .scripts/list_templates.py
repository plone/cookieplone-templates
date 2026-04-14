"""List templates declared in `cookieplone-config.json`.

Single source of truth for the list of templates used by both the
top-level ``Makefile`` (to iterate ``format`` / ``lint`` targets) and
the GitHub Actions matrix in ``.github/workflows/main.yml``.

Output modes:

* ``--format=paths`` (default): one path per line, relative to the
  repository root (e.g. ``templates/add-ons/backend``).  Suitable for
  ``$(shell ...)`` consumption in Make.
* ``--format=matrix``: JSON array of ``{"name": ..., "path": ...}``
  objects, suitable for ``fromJson(...)`` in a GitHub Actions
  ``strategy.matrix``.

Filter:

* ``--with-hooks``: only templates that have a ``hooks/`` subdirectory
  on disk (useful when iterating formatters that expect a hook source).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CONFIG_FILENAME = "cookieplone-config.json"


def _load_config(repo_root: Path) -> dict:
    config_path = repo_root / CONFIG_FILENAME
    return json.loads(config_path.read_text())


def _normalize_path(raw_path: str) -> str:
    """Strip the leading ``./`` from a template path."""
    return raw_path[2:] if raw_path.startswith("./") else raw_path


def collect_templates(
    config: dict,
    *,
    repo_root: Path | None = None,
    with_hooks: bool = False,
) -> list[dict[str, str]]:
    """Return ``[{name, path}, ...]`` for every template in *config*.

    When *with_hooks* is True, only templates that have a ``hooks``
    subdirectory on disk are returned (requires *repo_root*).
    """
    entries: list[dict[str, str]] = []
    for name, template in config.get("templates", {}).items():
        path = _normalize_path(template["path"])
        if (
            with_hooks
            and repo_root is not None
            and not (repo_root / path / "hooks").is_dir()
        ):
            continue
        entries.append({"name": name, "path": path})
    return entries


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--format",
        choices=("paths", "matrix"),
        default="paths",
        help="Output format (default: paths).",
    )
    parser.add_argument(
        "--with-hooks",
        action="store_true",
        help="Only emit templates that have a ``hooks/`` subdirectory on disk.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent.parent
    config = _load_config(repo_root)
    entries = collect_templates(
        config,
        repo_root=repo_root,
        with_hooks=args.with_hooks,
    )

    if args.format == "paths":
        print("\n".join(entry["path"] for entry in entries))
    else:
        print(json.dumps(entries))
    return 0


if __name__ == "__main__":
    sys.exit(main())
