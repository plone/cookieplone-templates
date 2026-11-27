"""Test cookiecutter generation for aurora_nick."""

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
    ".dockerignore",
    ".gitignore",
    ".prettierignore",
    ".prettierrc",
    "Dockerfile",
    "Makefile",
    "README.md",
    "babel.config.json",
    "config.ts",
    "docker-compose.yml",
    "eslint.config.ts",
    "mrs.developer.json",
    "package.json",
    "pnpm-workspace.yaml",
    "tsconfig.json",
]

BACKEND_ADDON_FILES = [
    "package.json",
    "src/index.ts",
    "src/migrations/.keep",
    "src/profiles/default/documents/_root.json",
    "src/profiles/default/groups.json",
    "src/profiles/default/index.ts",
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
    for file_path in BACKEND_FILES:
        path = cutter_result.project_path / "backend" / file_path
        assert path.exists()
        assert path.is_file()
    for file_path in BACKEND_ADDON_FILES:
        path = cutter_result.project_path / "backend/packages/nick-plone" / file_path
        assert path.exists()
        assert path.is_file()
    assert not (cutter_result.project_path / "backend/knexfile.ts").exists()
    assert not (cutter_result.project_path / "backend/src/profiles").exists()


def test_frontend_files_generated(cutter_result):
    """Check if the Aurora frontend workspace was generated."""
    for file_path in [
        ".pnpmfile.cjs",
        "Dockerfile",
        "eslint.config.mjs",
        "Makefile",
        "package.json",
        "pnpm-workspace.yaml",
        "registry.config.ts",
        "packages/aurora-plone/package.json",
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
    assert '"nick-plone": "workspace:*"' in package_json
    assert "@robgietema/nick" not in package_json

    config = (project_path / "backend/config.ts").read_text()
    assert "database: DB_NAME || 'nick'" in config
    assert "user: DB_USER || 'nick'" in config
    assert "password: DB_PASSWORD || 'nick'" in config
    assert "'@plone/nick:core'" in config
    assert "'nick-plone:default'" in config

    tsconfig = (project_path / "backend/tsconfig.json").read_text()
    assert '"@plone/nick": ["develop/nick/src"]' in tsconfig

    root_profile = (
        project_path
        / "backend/packages/nick-plone/src/profiles/default/documents/_root.json"
    ).read_text()
    assert "Welcome to Plone Aurora!" in root_profile
    assert "Welcome to Nick!" not in root_profile

    assert not (project_path / "backend/jsconfig.json").exists()
    assert not (project_path / "backend/eslint.config.mjs").exists()


def test_aurora_frontend_configuration(cutter_result):
    """Generate Aurora from the Aurora add-on scaffold without its standalone CI."""
    project_path = cutter_result.project_path
    package_json = (project_path / "frontend/package.json").read_text()
    assert '"@plone/aurora": "workspace:*"' in package_json
    assert "@plone/aurora dev" in package_json
    assert (project_path / "frontend/registry.config.ts").is_file()
    server_config = (
        project_path / "frontend/packages/aurora-plone/config/server.ts"
    ).read_text()
    assert "process.env.PLONE_API_PATH || 'http://localhost:8080'" in server_config
    assert not (project_path / ".github/workflows/acceptance.yml").exists()


def test_backend_addon(cutter_result):
    """The backend code and profiles are a Nick add-on in backend/packages."""
    addon_path = cutter_result.project_path / "backend/packages/nick-plone"
    package_json = (addon_path / "package.json").read_text()
    assert '"name": "nick-plone"' in package_json
    assert '"schema": "nick_plone"' in package_json
    assert '"@plone/nick": "workspace:^"' in package_json

    metadata = (addon_path / "src/profiles/default/metadata.json").read_text()
    assert '"id": "nick-plone:default"' in metadata
    assert '"dependencies": ["@plone/nick:core"]' in metadata

    workspace = (
        cutter_result.project_path / "backend/pnpm-workspace.yaml"
    ).read_text()
    assert "'packages/*'" in workspace


def test_backend_image(cutter_result):
    """The backend image adds the add-on to the official Nick image."""
    backend_path = cutter_result.project_path / "backend"
    dockerfile = (backend_path / "Dockerfile").read_text()
    assert "FROM plone/nick:${NICK_VERSION}" in dockerfile
    assert "COPY --chown=node:node packages /app/packages" in dockerfile
    assert 'pnpm add "nick-plone@workspace:*"' in dockerfile
    assert "ENV PROFILES=@plone/nick:core,nick-plone:default" in dockerfile

    backend_ci = (
        cutter_result.project_path / ".github/workflows/backend.yml"
    ).read_text()
    assert "container-image-build-push.yml" in backend_ci


def test_no_devops_scaffold(cutter_result):
    """Keep deployment and other monorepo extras out of this template."""
    project_path = cutter_result.project_path
    assert not (project_path / "devops").exists()
    assert not (project_path / "docker-compose.yml").exists()
