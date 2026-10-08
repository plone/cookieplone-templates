"""Test generation through the cookieplone CLI."""

EXPECTED_PATHS = {
    "app/package.json": True,
    "app/volto.config.js": True,
    "app/.github": False,
    "app/_project_files": False,
    "app/packages/volto-addon": False,
}


def test_cli_generation(bake_in_subprocess):
    """The post generation hook must find the add-ons/frontend template.

    The CLI runs hooks against a temporary copy of the template, so a path
    relative to the template folder cannot be resolved there (#476).
    The exit code is not checked: cookieplone 2.0.0 fails after generation
    while writing the answers file (plone/cookieplone#215).
    """
    result = bake_in_subprocess("sub/frontend_project", timeout=300)
    output = result.stdout + result.stderr
    assert "Hook script failed" not in output
    assert "could not be found in the primary location" not in output
    for file_path, exists in EXPECTED_PATHS.items():
        path = result.output_dir / file_path
        assert path.exists() is exists, file_path
