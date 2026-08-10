"""Test cookiecutter generation for volto_nick."""

ROOT_FILES = [
    ".editorconfig",
    ".gitignore",
    "CHANGELOG.md",
    "Makefile",
    "README.md",
    "dependabot.yml",
    "repository.toml",
    "towncrier.toml",
    "version.txt",
]

BACKEND_FILES = [
    ".gitignore",
    ".prettierignore",
    "Makefile",
    "README.md",
    "babel.config.json",
    "config.ts",
    "eslint.config.ts",
    "knexfile.ts",
    "mrs.developer.json",
    "package.json",
    "pnpm-workspace.yaml",
    "tsconfig.json",
]

BACKEND_PROJECT_FILES = [
    "src/events/index.ts",
    "src/migrations/.keep",
    "src/profiles/default/documents/_root.json",
    "src/profiles/default/groups.json",
    "src/profiles/default/metadata.json",
    "src/profiles/default/users.json",
]

CI_FILES = [
    "dependabot.yml",
    "workflows/backend.yml",
    "workflows/changelog.yml",
    "workflows/config.yml",
    "workflows/frontend.yml",
    "workflows/main.yml",
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


def test_backend_files_generated(cutter_result):
    """Check if Nick backend files were generated below backend/."""
    for file_path in BACKEND_FILES + BACKEND_PROJECT_FILES:
        path = cutter_result.project_path / "backend" / file_path
        assert path.exists()
        assert path.is_file()


def test_frontend_files_generated(cutter_result):
    """Check if the Volto frontend workspace was generated."""
    for file_path in [
        ".pnpmfile.cjs",
        "Makefile",
        "package.json",
        "pnpm-workspace.yaml",
        "packages/volto-plone/package.json",
    ]:
        assert (cutter_result.project_path / "frontend" / file_path).is_file()


def test_ci_files_generated(cutter_result):
    """Check that GitHub Actions were generated."""
    for file_path in CI_FILES:
        assert (cutter_result.project_path / ".github" / file_path).is_file()


def test_upstream_nick_configuration(cutter_result):
    """Generated configuration should use the current Plone Nick package."""
    project_path = cutter_result.project_path

    package_json = (project_path / "backend/package.json").read_text()
    assert '"@plone/nick": "workspace:^"' in package_json
    assert "@robgietema/nick" not in package_json

    config = (project_path / "backend/config.ts").read_text()
    assert "database: 'plone'" in config
    assert "'@plone/nick:core'" in config
    assert "'plone:default'" in config

    tsconfig = (project_path / "backend/tsconfig.json").read_text()
    assert '"@plone/nick": ["develop/nick/src"]' in tsconfig

    assert not (project_path / "backend/jsconfig.json").exists()
    assert not (project_path / "backend/eslint.config.mjs").exists()


def test_no_devops_scaffold(cutter_result):
    """Keep deployment and other monorepo extras out of this template."""
    project_path = cutter_result.project_path
    assert not (project_path / "devops").exists()
    assert not (project_path / "docker-compose.yml").exists()
