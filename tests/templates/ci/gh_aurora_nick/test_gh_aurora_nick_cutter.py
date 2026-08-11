"""Test generation of Aurora with Nick GitHub Actions."""

import pytest


def test_creation(cookies, template_path, context: dict):
    """Generate the .github folder."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == ".github"
    assert result.project_path.is_dir()


def test_variable_substitution(build_files_list, variable_pattern, cutter_result):
    """Check that no Cookieplone expressions remain."""
    for path in build_files_list(cutter_result.project_path):
        with open(path) as fh:
            for line in fh:
                match = {pattern.search(line) for pattern in variable_pattern}
                assert match == {None}, f"cookiecutter variable not replaced in {path}"


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        ["workflows/backend.yml", "github-workflow"],
        ["workflows/changelog.yml", "github-workflow"],
        ["workflows/config.yml", "github-workflow"],
        ["workflows/frontend.yml", "github-workflow"],
        ["workflows/main.yml", "github-workflow"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    """Validate generated workflows."""
    assert schema_validate_file(cutter_result.project_path / file_path, schema_name)


@pytest.mark.parametrize(
    "file_path",
    [
        "dependabot.yml",
        "workflows/backend.yml",
        "workflows/changelog.yml",
        "workflows/config.yml",
        "workflows/frontend.yml",
        "workflows/main.yml",
    ],
)
def test_created_files(cutter_result, file_path: str):
    """Generate all CI files."""
    assert (cutter_result.project_path / file_path).is_file()


def test_node_workspaces_do_not_use_python_backend_ci(cutter_result):
    """Keep the Nick checks on the Node toolchain."""
    contents = (cutter_result.project_path / "workflows/backend.yml").read_text()
    assert "actions/setup-node@" in contents
    assert "backend-pytest" not in contents
    assert "repoplone" not in contents


def test_frontend_uses_aurora_ci(cutter_result):
    """Run the checks supported by the Aurora workspace."""
    frontend = (cutter_result.project_path / "workflows/frontend.yml").read_text()
    assert "npm install --global corepack@latest" in frontend
    assert "make install" in frontend
    assert "make lint" in frontend
    assert "make test" in frontend
    assert "make build" in frontend
    assert "frontend-unit.yml" not in frontend
