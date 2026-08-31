"""Test repository-level GitHub Actions workflows."""

from pathlib import Path

import yaml


def test_main_workflow_schema(schema_validate_file):
    """Validate the main GitHub Actions workflow."""
    path = Path(__file__).parents[2] / ".github/workflows/main.yml"
    assert schema_validate_file(path, "github-workflow")


def test_all_functional_jobs_run_generated_developer_commands():
    """Exercise the generated project's day-one lint and test commands."""
    root = Path(__file__).parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/main.yml").read_text())
    functional_jobs = {
        name: job
        for name, job in workflow["jobs"].items()
        if name.endswith("-functional") or name.endswith("-functional-prerelease")
    }

    assert functional_jobs
    for name, job in functional_jobs.items():
        commands = {
            line.strip()
            for step in job["steps"]
            for line in step.get("run", "").splitlines()
        }
        assert "make lint" in commands, name
        assert "make test" in commands, name


def test_volto_nick_functional_job():
    """Exercise the generated Volto and Nick project together."""
    root = Path(__file__).parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/main.yml").read_text())
    job = workflow["jobs"]["volto-nick-functional"]

    assert job["services"]["postgres"]["image"] == "postgres:16"
    assert job["env"]["template"] == "volto_nick"
    assert "volto-nick-functional" in workflow["jobs"]["report"]["needs"]

    steps = {step.get("name"): step for step in job["steps"]}
    assert steps["Lint generated project"]["run"].strip() == "make lint"
    assert steps["Test generated project"]["run"].strip() == "make test"

    background_step = next(
        step
        for step in job["steps"]
        if step.get("uses") == "JarvusInnovations/background-action@v2"
    )
    assert "make backend-start &" in background_step["with"]["run"]
    assert "make frontend-start &" in background_step["with"]["run"]
    assert "http://localhost:3000" in background_step["with"]["wait-on"]
    assert (root / ".github/tests/volto-nick.test.js").is_file()


def test_aurora_nick_functional_job():
    """Exercise the generated Aurora and Nick project together."""
    root = Path(__file__).parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/main.yml").read_text())
    job = workflow["jobs"]["aurora-nick-functional"]

    assert job["services"]["postgres"]["image"] == "postgres:16"
    assert job["env"]["template"] == "aurora_nick"
    assert "aurora-nick-functional" in workflow["jobs"]["report"]["needs"]

    background_step = next(
        step
        for step in job["steps"]
        if step.get("uses") == "JarvusInnovations/background-action@v2"
    )
    assert background_step["env"]["PLONE_API_PATH"] == "http://localhost:8080"
    assert "make backend-start &" in background_step["with"]["run"]
    assert "pnpm build && pnpm start:prod" in background_step["with"]["run"]
    assert "make frontend-start &" not in background_step["with"]["run"]
    assert "http://localhost:3000" in background_step["with"]["wait-on"]

    playwright_step = next(
        step for step in job["steps"] if step.get("name") == "Install Playwright"
    )
    assert "pnpm add" not in playwright_step["run"]
    assert "pnpm exec playwright install" in playwright_step["run"]
    assert (root / ".github/tests/aurora-nick.test.js").is_file()


def test_aurora_cmfplone_functional_job():
    """Exercise the generated Aurora and Python Plone project together."""
    root = Path(__file__).parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/main.yml").read_text())
    job = workflow["jobs"]["aurora-cmfplone-functional"]

    assert "services" not in job
    assert job["env"]["template"] == "aurora_cmfplone"
    assert job["env"]["python-version"] == "3.13"
    assert "aurora-cmfplone-functional" in workflow["jobs"]["report"]["needs"]

    install_step = next(
        step for step in job["steps"] if step.get("name") == "Install generated project"
    )
    assert "make install" in install_step["run"]

    background_step = next(
        step
        for step in job["steps"]
        if step.get("uses") == "JarvusInnovations/background-action@v2"
    )
    assert background_step["env"]["PLONE_API_PATH"] == (
        "http://localhost:8080/Plone"
    )
    assert "make backend-start &" in background_step["with"]["run"]
    assert "pnpm build && pnpm start:prod" in background_step["with"]["run"]
    assert "http-get://localhost:8080/Plone" in background_step["with"]["wait-on"]
    assert "http://localhost:3000" in background_step["with"]["wait-on"]

    playwright_step = next(
        step for step in job["steps"] if step.get("name") == "Install Playwright"
    )
    assert "pnpm exec playwright install" in playwright_step["run"]
    assert (root / ".github/tests/aurora-cmfplone.test.js").is_file()


def test_background_actions_use_v2():
    """Use the Node.js 24-compatible background action release."""
    root = Path(__file__).parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/main.yml").read_text())
    actions = [
        step["uses"]
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
        if step.get("uses", "").startswith("JarvusInnovations/background-action@")
    ]

    assert actions
    assert set(actions) == {"JarvusInnovations/background-action@v2"}
