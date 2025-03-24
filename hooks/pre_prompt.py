"""Pre Prompt hook."""

import sys

try:
    from cookieplone import __version__
    from cookieplone.utils import console, versions

except ModuleNotFoundError:
    __version__ = ""


MIN_COOKIEPLONE = "0.8.0.dev0"


def _check_version(version: str) -> str:
    msg = ""
    if not version:
        msg = "This template should be run with cookieplone"
    else:
        v = versions.Version(version)
        min_v = versions.Version(MIN_COOKIEPLONE)
        is_valid = versions.is_valid_version(v, min_v, allow_prerelease=True)
        if not is_valid:
            msg = f"Please upgrade Cookieplone to {MIN_COOKIEPLONE} or higher."
    return msg


def main():
    """Check if we have cookieplone installed."""
    if _check_version(__version__):
        print()
        sys.exit(1)
    else:
        console.print_plone_banner()


if __name__ == "__main__":
    main()
