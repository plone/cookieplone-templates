"""Test generation through the cookieplone CLI."""

EXPECTED_PATHS = {
    "app/package.json": True,
    "app/registry.config.ts": True,
    "app/.github": False,
    "app/_project_files": False,
    "app/packages/aurora-addon": False,
}


def test_cli_generation(bake_in_subprocess):
    """The post generation hook must find the add-ons/aurora_addon template.

    The exit code is not checked: cookieplone 2.0.0 fails after generation
    while writing the answers file (plone/cookieplone#215).
    """
    result = bake_in_subprocess("sub/aurora_project", timeout=300)
    output = result.stdout + result.stderr
    assert "Hook script failed" not in output
    assert "could not be found in the primary location" not in output
    for file_path, exists in EXPECTED_PATHS.items():
        path = result.output_dir / file_path
        assert path.exists() is exists, file_path
