"""Shared expectations for the CI template test suites."""

CHANGELOG_WORKFLOW = "workflows/changelog.yml"
CONFIG_WORKFLOW = "workflows/config.yml"

# The changelog workflow used to install the whole frontend toolchain only to
# reach the towncrier template shipped in `node_modules/@plone/scripts`. That
# template now lives inside each codebase, so none of this should remain.
FRONTEND_TOOLING = [
    "actions/setup-node",
    "corepack",
    "pnpm",
    "make install",
    "STORE_PATH",
    "NODE_VERSION",
]

# Codebases a CI template may check, and the towncrier config file each one uses.
TOWNCRIER_CONFIG_FILE = {
    "backend": "pyproject.toml",
    "frontend": "towncrier.toml",
    "repository": "towncrier.toml",
}


def step_id(codebase: str) -> str:
    """Return the id of the step checking a codebase.

    :param codebase: One of ``backend``, ``frontend`` or ``repository``.
    :returns: The step id used in the changelog workflow.
    """
    return f"{codebase}-changelog"


def changelog_flag(codebase: str) -> str:
    """Return the config output guarding the check of a codebase.

    :param codebase: One of ``backend``, ``frontend`` or ``repository``.
    :returns: Name of the ``config`` workflow output.
    """
    return f"changelog-{codebase}"
