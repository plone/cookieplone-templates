"""Shared expectations for the template test suites."""

# Filename of the towncrier template shipped inside each codebase.
CHANGELOG_TEMPLATE_NAME = ".changelog_template.jinja"

# Settings every towncrier configuration must share, regardless of the codebase
# (backend, frontend or project) it belongs to. ``issue_format`` is excluded
# because it embeds the repository URL -- use :func:`expected_settings`.
TOWNCRIER_SETTINGS = {
    "filename": "CHANGELOG.md",
    "directory": "news/",
    "title_format": "## {version} ({project_date})",
    "underlines": ["", "", ""],
    "start_string": "<!-- towncrier release notes start -->\n",
}

# News fragment types, shared by backend, frontend and project codebases.
TOWNCRIER_TYPES = {
    "breaking": "Breaking",
    "feature": "Feature",
    "bugfix": "Bugfix",
    "internal": "Internal",
    "documentation": "Documentation",
    "tests": "Tests",
}


def expected_issue_format(repository_url: str) -> str:
    """Return the ``issue_format`` expected for a given repository.

    :param repository_url: Base URL of the generated repository.
    :returns: The towncrier ``issue_format`` setting.
    """
    return f"[#{{issue}}]({repository_url}/issues/{{issue}})"


def expected_settings(repository_url: str) -> dict:
    """Return every towncrier setting expected for a given repository.

    :param repository_url: Base URL of the generated repository.
    :returns: Mapping of towncrier setting to its expected value.
    """
    return {
        **TOWNCRIER_SETTINGS,
        "issue_format": expected_issue_format(repository_url),
    }
