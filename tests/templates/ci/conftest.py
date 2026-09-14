"""Pytest configuration shared by the CI template test suites."""

import pytest

from tests.templates.ci import CHANGELOG_WORKFLOW, CONFIG_WORKFLOW


@pytest.fixture
def changelog(cutter_result, github_workflow) -> dict:
    """Parsed changelog workflow."""
    return github_workflow(cutter_result.project_path / CHANGELOG_WORKFLOW)


@pytest.fixture
def changelog_text(cutter_result) -> str:
    """Raw content of the changelog workflow."""
    return (cutter_result.project_path / CHANGELOG_WORKFLOW).read_text()


@pytest.fixture
def config(cutter_result, github_workflow) -> dict:
    """Parsed config workflow."""
    return github_workflow(cutter_result.project_path / CONFIG_WORKFLOW)


@pytest.fixture
def checks_steps(changelog) -> list:
    """Steps of the ``checks`` job of the changelog workflow."""
    return changelog["jobs"]["checks"]["steps"]
