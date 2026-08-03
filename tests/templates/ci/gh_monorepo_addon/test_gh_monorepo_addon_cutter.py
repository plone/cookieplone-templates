"""Test cookieplone generation with all features enabled."""

import pytest


def test_creation(cookies, template_path, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context, template=template_path)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == ".github"
    assert result.project_path.is_dir()


def test_variable_substitution(build_files_list, variable_pattern, cutter_result):
    """Check if no file was unprocessed."""
    paths = build_files_list(cutter_result.project_path)
    for path in paths:
        with open(path) as fh:
            for line in fh:
                match = {pattern.search(line) for pattern in variable_pattern}
                msg = f"cookiecutter variable not replaced in {path}"
                assert match == {None}, msg


@pytest.mark.parametrize(
    "file_path,schema_name",
    [
        ["workflows/changelog.yml", "github-workflow"],
        ["workflows/config.yml", "github-workflow"],
        ["workflows/frontend.yml", "github-workflow"],
        ["workflows/backend.yml", "github-workflow"],
        ["workflows/main.yml", "github-workflow"],
    ],
)
def test_json_schema(
    cutter_result, schema_validate_file, file_path: str, schema_name: str
):
    path = cutter_result.project_path / file_path
    assert schema_validate_file(path, schema_name)


@pytest.mark.parametrize(
    "file_path",
    [
        "instructions/general/docs.md",
        "instructions/docs.instructions.md",
        "instructions/volto.instructions.md",
        "workflows/changelog.yml",
        "workflows/backend.yml",
        "workflows/config.yml",
        "workflows/frontend.yml",
        "workflows/main.yml",
    ],
)
def test_created_files(cutter_result, file_path: str):
    path = (cutter_result.project_path / file_path).resolve()
    assert path.exists()
    assert path.is_file()


@pytest.mark.parametrize(
    "file_path,text,expected",
    [
        (
            "workflows/changelog.yml",
            "uvx towncrier check  --compare-with origin/${{ env.BASE_BRANCH }}",
            True,
        ),
        ("workflows/changelog.yml", "pipx", False),
        (
            "workflows/config.yml",
            "echo 'plone-version: ${{ steps.vars.outputs.plone-version }}",
            True,
        ),
        (
            "workflows/config.yml",
            "image-name-prefix=$(jq -r '.container_images_prefix'",
            True,
        ),
        ("workflows/main.yml", "uses: ./.github/workflows/config.yml", True),
        (
            "workflows/config.yml",
            "storybook-deploy=${{ github.event.repository.private == false }}",
            True,
        ),
        (
            "workflows/main.yml",
            "storybook-deploy: ${{ needs.config.outputs.storybook-deploy }}",
            True,
        ),
    ],
)
def test_content(cutter_result, file_path: str, text: str, expected: bool):
    path = (cutter_result.project_path / file_path).resolve()
    contents = path.read_text()
    assert (text in contents) is expected
