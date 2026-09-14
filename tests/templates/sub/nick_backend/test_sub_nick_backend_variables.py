ALLOWED_MISSING = []
ALLOWED_NOT_USED = []


def test_no_missing_variables(variables_missing):
    """Test no variable is missing from cookieplone.json."""
    assert variables_missing == ALLOWED_MISSING


def test_not_used_variables(variables_not_used):
    """Test variables are used."""
    assert variables_not_used == ALLOWED_NOT_USED
