"""Post generation hook."""

from collections import OrderedDict
from pathlib import Path
from typing import Callable

from cookieplone.utils import console, plone

context: OrderedDict = {{cookiecutter}}


def update_file(filepath: Path, func: Callable, content: str) -> Path:
    src_data = filepath.read_text()
    filepath.write_text(func(content, src_data))
    return filepath


def set_configurations(package_root: Path, context: OrderedDict):
    """Adjust dependencies.zcml and profiles/default/metadata.xml."""
    info = [
        (
            "profiles/default/metadata.xml",
            plone.add_dependency_profile_to_metadata,
            "plone.app.caching:default",
        ),
        (
            "profiles/default/metadata.xml",
            plone.add_dependency_profile_to_metadata,
            "plone.app.caching:with-caching-proxy",
        ),
        ("dependencies.zcml", plone.add_dependency_to_zcml, "plone.app.caching"),
    ]
    for path, func, content in info:
        filepath: Path = package_root / path
        if filepath.exists():
            filepath = update_file(filepath, func, content)


def main():
    """Final fixes."""
    output_dir = Path().cwd()
    package_root = output_dir / "backend/src/packagename"
    set_configurations(package_root, context)


if __name__ == "__main__":
    main()
