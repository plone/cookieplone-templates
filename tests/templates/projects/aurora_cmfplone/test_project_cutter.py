"""Test cookiecutter generation."""

import json
from pathlib import Path

import pytest


def build_files_list(root_dir: Path) -> list[Path]:
    """Build a list containing absolute paths to the generated files."""
    return [path for path in Path(root_dir).glob("*") if path.is_file()]


def test_default_configuration(cookies, template_path, context: dict):
    """Generated project should replace all variables."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()


def test_variable_substitution(cutter_result, variable_pattern):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        with open(path) as fh:
            for line in fh:
                match = {pattern.search(line) for pattern in variable_pattern}
                msg = f"cookiecutter variable not replaced in {path}"
                assert match == {None}, msg


FOLDERS = [
    ".github",
    ".vscode",
    "backend",
    "devops",
    "frontend",
]


@pytest.mark.parametrize("folder_name", FOLDERS)
def test_root_folders(cutter_result, folder_name: str):
    """Test folders were created."""
    folder = cutter_result.project_path / folder_name
    assert folder.is_dir()


def test_git_initialization(cutter_result):
    from cookieplone.utils import git

    path = cutter_result.project_path
    repo = git.repo_from_path(path)
    assert Path(repo.working_dir) == path


def test_git_initialization_not_set(cookies, template_path, context_no_git):
    from cookieplone.utils import git

    cutter_result = cookies.bake(extra_context=context_no_git, template=template_path)
    path = cutter_result.project_path
    assert git.check_path_is_repository(path) is False


@pytest.mark.parametrize(
    "file_path",
    [
        ".pnpmfile.cjs",
        "Dockerfile",
        "Makefile",
        "package.json",
        "pnpm-workspace.yaml",
        "registry.config.ts",
        "packages/aurora-ploneorgbr/package.json",
    ],
)
def test_aurora_frontend_files(cutter_result, file_path: str):
    """Generate the Aurora workspace from the Aurora add-on subtemplate."""
    assert (cutter_result.project_path / "frontend" / file_path).is_file()


def test_aurora_frontend_configuration(cutter_result):
    """Keep Aurora configured without unsupported repoplone metadata."""
    project = cutter_result.project_path
    package = json.loads((project / "frontend/package.json").read_text())
    repository = (project / "repository.toml").read_text()
    assert package["dependencies"]["@plone/aurora"] == "workspace:*"
    assert package["packageManager"] == "pnpm@11.20.0"
    assert "[frontend.package]" not in repository
    assert "@plone/volto" not in repository
    assert 'base_package = "Products.CMFPlone"' in repository
    makefile = (project / "frontend/Makefile").read_text()
    assert "REPOSITORY_SETTINGS :=" not in makefile
    assert "pnpm dlx mrs-developer" in makefile
    assert not (project / "frontend/volto.config.js").exists()


def test_python_backend_and_aurora_ci(cutter_result):
    """Combine the monorepo Python backend CI with Aurora frontend checks."""
    workflows = cutter_result.project_path / ".github/workflows"
    backend = (workflows / "backend.yml").read_text()
    frontend = (workflows / "frontend.yml").read_text()
    config = (workflows / "config.yml").read_text()
    makefile = (cutter_result.project_path / "Makefile").read_text()
    assert "backend-pytest.yml" in backend
    assert 'name: "Frontend: Lint, test, and build"' in frontend
    assert "@plone/aurora" not in backend
    assert "frontend-base-version" in config
    assert "FRONTEND_BASE_VERSION" in makefile
    assert "volto_version" not in config
    assert "volto_version" not in makefile
