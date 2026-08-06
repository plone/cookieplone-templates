"""Shared tests for the changelog workflow of every CI template.

Import them into a suite with::

    from tests.templates.ci.changelog import *  # noqa: F403

Each suite provides its own data through the ``codebases``, ``guarded`` and
``expects_python_version`` fixtures.
"""

import re

import pytest

from tests.templates.ci import (
    CHANGELOG_WORKFLOW,
    FRONTEND_TOOLING,
    TOWNCRIER_CONFIG_FILE,
    changelog_flag,
    step_id,
)


def test_changelog_workflow_generated(cutter_result):
    """Test the changelog workflow is generated."""
    path = cutter_result.project_path / CHANGELOG_WORKFLOW
    assert path.is_file()


def test_changelog_jobs(changelog):
    """Test the workflow declares a config and a checks job."""
    assert set(changelog["jobs"]) == {"config", "checks"}


def test_config_job_reuses_config_workflow(changelog):
    """Test the config job delegates to the reusable config workflow."""
    assert changelog["jobs"]["config"]["uses"] == "./.github/workflows/config.yml"


def test_config_job_honors_skip_label(changelog):
    """Test the whole workflow can be skipped with a label."""
    assert "skip changelog" in changelog["jobs"]["config"]["if"]


def test_checks_job_needs_config(changelog):
    """Test the checks job consumes the config job outputs."""
    assert changelog["jobs"]["checks"]["needs"] == ["config"]


def test_checks_job_python_version_from_config(checks_steps, expects_python_version):
    """Test the Python version comes from the config workflow.

    Hardcoding it here would drift from ``cookiecutter.python_version``.
    """
    setup = [step for step in checks_steps if "setup_uv" in step.get("uses", "")]
    assert setup, "no setup_uv step found"
    version = setup[0]["with"].get("python-version")
    if not expects_python_version:
        assert version is None
        return
    assert version == "${{ needs.config.outputs.python-version }}"


def test_fetch_base_branch_step(checks_steps):
    """Test the base branch is fetched, so towncrier can compare against it."""
    fetch = [step for step in checks_steps if "git fetch" in step.get("run", "")]
    assert fetch, "no step fetching the base branch"
    assert "origin ${{ env.base-branch }}" in fetch[0]["run"]


@pytest.mark.parametrize("tooling", FRONTEND_TOOLING)
def test_no_frontend_tooling(changelog_text, tooling: str):
    """Test the workflow no longer installs the frontend toolchain."""
    assert tooling not in changelog_text


def test_check_steps_generated(changelog, workflow_step, codebases):
    """Test every codebase of this template is checked."""
    for codebase, _ in codebases:
        step = workflow_step(changelog, "checks", step_id(codebase))
        assert step, f"no check step for {codebase}"


def test_check_steps_are_the_only_ones(changelog, workflow_step, codebases):
    """Test no codebase is checked twice, and none is left behind."""
    ids = {step.get("id") for step in changelog["jobs"]["checks"]["steps"]}
    ids.discard(None)
    assert ids == {step_id(codebase) for codebase, _ in codebases}


def test_check_steps_towncrier_command(changelog, workflow_step, codebases):
    """Test the towncrier invocation of every codebase is well formed.

    ``--config`` and ``--dir`` must each be followed by a space, otherwise the
    expression is glued to the flag and towncrier receives a single, bogus
    argument.
    """
    for codebase, path_output in codebases:
        run = workflow_step(changelog, "checks", step_id(codebase))["run"]
        config_file = TOWNCRIER_CONFIG_FILE[codebase]
        assert re.search(
            rf"--config \$\{{\{{ needs\.config\.outputs\.{path_output} \}}\}}"
            rf"/{config_file}",
            run,
        ), f"bad --config for {codebase}: {run}"
        assert re.search(
            rf"--dir \$\{{\{{ needs\.config\.outputs\.{path_output} \}}\}}", run
        ), f"bad --dir for {codebase}: {run}"
        assert "--compare-with origin/${{ env.base-branch }}" in run


def test_check_steps_guard(changelog, workflow_step, codebases, guarded):
    """Test each check only runs when its codebase changed.

    Single codebase templates have nothing to filter, so they run unguarded.
    """
    for codebase, _ in codebases:
        step = workflow_step(changelog, "checks", step_id(codebase))
        condition = step.get("if", "")
        if not guarded:
            assert not condition, f"{codebase} should run unconditionally"
            continue
        assert f"needs.config.outputs.{changelog_flag(codebase)} == 'true'" in condition
        # `always()` keeps a failing codebase from masking the remaining ones.
        assert "always()" in condition


def test_report_step_generated(changelog, codebases):
    """Test the workflow reports the conclusion of every check."""
    steps = changelog["jobs"]["checks"]["steps"]
    report = next(item for item in steps if item.get("name") == "Report check")
    for codebase, _ in codebases:
        assert f"steps.{step_id(codebase)}.conclusion" in report["run"]


def test_config_workflow_declares_path_outputs(config, codebases):
    """Test the config workflow exposes the path of every codebase."""
    outputs = config["on"]["workflow_call"]["outputs"]
    job_outputs = config["jobs"]["config"]["outputs"]
    for _, path_output in codebases:
        assert path_output in outputs
        assert path_output in job_outputs


def test_config_workflow_declares_changelog_flags(config, codebases, guarded):
    """Test the config workflow exposes a flag for every checked codebase."""
    if not guarded:
        pytest.skip("single codebase templates do not filter by path")
    outputs = config["on"]["workflow_call"]["outputs"]
    job_outputs = config["jobs"]["config"]["outputs"]
    for codebase, _ in codebases:
        assert changelog_flag(codebase) in outputs
        assert changelog_flag(codebase) in job_outputs


def test_config_workflow_declares_filters(config, workflow_step, codebases, guarded):
    """Test the paths filter computes a flag for every checked codebase."""
    if not guarded:
        pytest.skip("single codebase templates do not filter by path")
    filters = workflow_step(config, "config", "filter")["with"]["filters"]
    for codebase, _ in codebases:
        assert f"{changelog_flag(codebase)}:" in filters
