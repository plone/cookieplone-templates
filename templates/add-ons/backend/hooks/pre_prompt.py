"""Pre Prompt hook."""

import sys

try:
    from cookieplone import __version__ as cookieplone_version
    from cookieplone import data
    from cookieplone.utils import commands, console, sanity
except ModuleNotFoundError:
    print("This template should be run with cookieplone")
    sys.exit(1)
from packaging.version import Version

SUPPORTED_PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]
MIN_COOKIEPLONE = "0.9.6"
COOKIEPLONE_INSTALLATION = (
    "https://github.com/plone/cookieplone/blob/main/README.md#installation-"
)


def sanity_check() -> data.SanityCheckResults:
    """Run sanity checks on the system."""
    checks = [
        data.SanityCheck(
            "Cookieplone",
            lambda: (
                ""
                if Version(cookieplone_version) >= Version(MIN_COOKIEPLONE)
                else (
                    f"This template requires Cookieplone {MIN_COOKIEPLONE} "
                    "or higher. Upgrade information available "
                    f"at {COOKIEPLONE_INSTALLATION}."
                )
            ),
            [],
            "error",
        ),
        data.SanityCheck(
            "UV",
            commands.check_command_is_available,
            ["uv"],
            "error",
        ),
        data.SanityCheck("git", commands.check_command_is_available, ["git"], "error"),
    ]
    return sanity.run_sanity_checks(checks)


def main():
    """Validate context."""

    msg = """
Creating a new Plone Addon

Sanity check results:
"""
    check_results = sanity_check()
    for check in check_results.checks:
        label = "green" if check.status else "red"
        msg = f"{msg}\n  - {check.name}: [{label}]{check.message}[/{label}]"
    console.panel(title="Plone Addon", msg=f"{msg}\n")
    if not check_results.status:
        sys.exit(1)


if __name__ == "__main__":
    main()
