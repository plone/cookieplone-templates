ALLOWED_MISSING = []
ALLOWED_NOT_USED = []


def test_no_missing_variables(variables_missing):
    """Test no variable is missing from cookiecutter.json"""
    assert len(variables_missing) == len(ALLOWED_MISSING)
    assert variables_missing == ALLOWED_MISSING


def test_not_used_variables(variables_not_used):
    """Test variables are used."""
    assert len(variables_not_used) == len(ALLOWED_NOT_USED)
    assert variables_not_used == ALLOWED_NOT_USED
