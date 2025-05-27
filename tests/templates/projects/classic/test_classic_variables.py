ALLOWED_MISSING = ["feature_headless", "frontend_addon_name", "initialize_git", "volto_version"]
ALLOWED_NOT_USED = ["__devops_host", "__devops_swarm_public_network", "__devops_traefik_docker_network", "__devops_traefik_stack_include_ui", "__gha_version_setup_node", "__node_version", "__npm_package_name", "__version_frontend_package", "__version_mrs_developer", "__version_plone_scripts", "__version_plone_volto", "__version_pnpm", "__version_release_it"]


def test_no_missing_variables(variables_missing):
    """Test no variable is missing from cookiecutter.json"""
    assert len(variables_missing) == len(ALLOWED_MISSING)
    assert variables_missing == ALLOWED_MISSING


def test_not_used_variables(variables_not_used):
    """Test variables are used."""
    assert len(variables_not_used) == len(ALLOWED_NOT_USED)
    assert variables_not_used == ALLOWED_NOT_USED
