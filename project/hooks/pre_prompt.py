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

SUPPORTED_PYTHON_VERSIONS = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
]


def sanity_check() -> data.SanityCheckResults:
    """Run sanity checks on the system."""
    checks = [
        data.SanityCheck(
            "Cookieplone",
            lambda: (
                ""
                if Version(cookieplone_version) > Version("0.8.0.dev0")
                else "This template requires Cookieplone 0.8 or higher."
            ),
            [],
            "error",
        ),
        data.SanityCheck(
            "Python",
            commands.check_python_version,
            [SUPPORTED_PYTHON_VERSIONS],
            "error",
        ),
        data.SanityCheck(
            "Node",
            commands.check_node_version,
            [],
            "error",
        ),
        data.SanityCheck("git", commands.check_command_is_available, ["git"], "error"),
        data.SanityCheck(
            "Docker (optional)", commands.check_docker_version, ["26"], "warning"
        ),
    ]
    return sanity.run_sanity_checks(checks)


def main():
    """Validate context."""

    msg = """
Creating a new Plone Project

Sanity check results:
"""
    check_results = sanity_check()
    for check in check_results.checks:
        label = "green" if check.status else "red"
        msg = f"{msg}\n  - {check.name}: [{label}]{check.message}[/{label}]"
    console.panel(title="Plone Project", msg=f"{msg}\n")
    if not check_results.status:
        sys.exit(1)


if __name__ == "__main__":
    main()
