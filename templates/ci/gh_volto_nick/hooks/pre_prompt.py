"""Pre-prompt hook."""

import sys

try:
    from cookieplone import __version__
    from cookieplone.utils import versions
except ModuleNotFoundError:
    __version__ = ""


MIN_COOKIEPLONE = "2.0.0a2"
COOKIEPLONE_INSTALLATION = (
    "https://github.com/plone/cookieplone/blob/main/README.md#installation-"
)


def _check_version(version: str) -> str:
    """Return an error message when Cookieplone is missing or too old."""
    if not version:
        return "This template should be run with cookieplone"

    current = versions.Version(version)
    minimum = versions.Version(MIN_COOKIEPLONE)
    if not versions.is_valid_version(current, minimum, allow_prerelease=True):
        return (
            f"This template requires Cookieplone {MIN_COOKIEPLONE} or higher. "
            f"Upgrade information available at {COOKIEPLONE_INSTALLATION}."
        )
    return ""


def main():
    """Check the Cookieplone version."""
    if msg := _check_version(__version__):
        print(msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
