"""Pre Prompt hook."""

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
    msg = ""
    if not version:
        msg = "This template should be run with cookieplone"
    else:
        v = versions.Version(version)
        min_v = versions.Version(MIN_COOKIEPLONE)
        is_valid = versions.is_valid_version(v, min_v, allow_prerelease=True)
        if not is_valid:
            msg = (
                f"This template requires Cookieplone {MIN_COOKIEPLONE} "
                "or higher. Upgrade information available "
                f"at {COOKIEPLONE_INSTALLATION}."
            )
    return msg


def main():
    """Check if we have cookieplone installed."""
    if msg := _check_version(__version__):
        print(msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
