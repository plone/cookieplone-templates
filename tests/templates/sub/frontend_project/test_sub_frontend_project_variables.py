# Used by the add-ons/frontend subtemplate, which computes them itself
# or receives them from the post generation hook.
ALLOWED_MISSING = [
    "description",
    "frontend_addon_name",
    "github_organization",
    "initialize_ci",
    "initialize_documentation",
    "npm_package_name",
    "use_prerelease_versions",
]
ALLOWED_NOT_USED = ["__generator_sha"]


def test_no_missing_variables(variables_missing):
    """Test no variable is missing from cookiecutter.json"""
    assert len(variables_missing) == len(ALLOWED_MISSING)
    assert variables_missing == ALLOWED_MISSING


def test_not_used_variables(variables_not_used):
    """Test variables are used."""
    assert len(variables_not_used) == len(ALLOWED_NOT_USED)
    assert variables_not_used == ALLOWED_NOT_USED
