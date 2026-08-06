"""Test repository-level GitHub Actions workflows."""

from pathlib import Path

import yaml


def test_main_workflow_schema(schema_validate_file):
    """Validate the main GitHub Actions workflow."""
    path = Path(__file__).parents[2] / ".github/workflows/main.yml"
    assert schema_validate_file(path, "github-workflow")


def test_volto_nick_functional_job():
    """Exercise the generated Volto and Nick project together."""
    root = Path(__file__).parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/main.yml").read_text())
    job = workflow["jobs"]["volto-nick-functional"]

    assert job["services"]["postgres"]["image"] == "postgres:16"
    assert job["env"]["template"] == "volto_nick"
    assert "volto-nick-functional" in workflow["jobs"]["report"]["needs"]

    background_step = next(
        step
        for step in job["steps"]
        if step.get("uses") == "JarvusInnovations/background-action@v1.0.7"
    )
    assert "make backend-start &" in background_step["with"]["run"]
    assert "make frontend-start &" in background_step["with"]["run"]
    assert "http://localhost:3000" in background_step["with"]["wait-on"]
    assert (root / ".github/tests/volto-nick.spec.js").is_file()
