"""Test cookiecutter generation for plone7_nick."""

ROOT_FILES = [
    ".gitignore",
    ".prettierignore",
    "Makefile",
    "README.md",
    "babel.config.json",
    "config.ts",
    "eslint.config.mjs",
    "jsconfig.json",
    "knexfile.ts",
    "mrs.developer.json",
    "package.json",
    "pnpm-workspace.yaml",
    "tsconfig.json",
]

PROJECT_FILES = [
    "src/events/index.ts",
    "src/migrations/.keep",
    "src/profiles/default/documents/_root.json",
    "src/profiles/default/groups.json",
    "src/profiles/default/metadata.json",
    "src/profiles/default/users.json",
]


def test_creation(cookies, context: dict):
    """Generated project should match provided value."""
    result = cookies.bake(extra_context=context)
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.name == context["project_slug"]
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


def test_root_files_generated(cutter_result):
    """Check if root files were generated."""
    for file_path in ROOT_FILES:
        path = cutter_result.project_path / file_path
        assert path.exists()
        assert path.is_file()


def test_project_files_generated(cutter_result):
    """Check if project files were generated."""
    for file_path in PROJECT_FILES:
        path = cutter_result.project_path / file_path
        assert path.exists()
        assert path.is_file()
