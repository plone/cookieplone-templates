"""Pre Prompt hook."""

import sys
from textwrap import dedent

try:
    from cookieplone import __version__ as cookieplone_version
    from cookieplone import data
    from cookieplone.utils import commands, console, sanity
except ModuleNotFoundError:
    print("This template should be run with cookieplone")
    sys.exit(1)
from packaging.version import Version


SUPPORTED_NODE_VERSIONS = [
    "18",
    "19",
    "20",
    "21",
    "22",
    "24",
]
MIN_COOKIEPLONE = "2.0.0a2"
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
            "Node",
            commands.check_node_version,
            [SUPPORTED_NODE_VERSIONS],
            "error",
        ),
        data.SanityCheck("git", commands.check_command_is_available, ["git"], "error"),
    ]
    result = sanity.run_sanity_checks(checks)
    return result


def main():
    """Validate context."""
    check_results = sanity_check()
    msg = dedent(
        """
        Creating a new Seven Addon

        Sanity check results:

    """
    )
    for check in check_results.checks:
        label = "green" if check.status else "red"
        msg = f"{msg}\n  - {check.name}: [{label}]{check.message}[/{label}]"
    console.panel(title="Volto Addon Generator", msg=f"{msg}\n")
    if not check_results.status:
        sys.exit(1)


if __name__ == "__main__":
    main()
