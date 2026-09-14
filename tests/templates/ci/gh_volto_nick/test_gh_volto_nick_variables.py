ALLOWED_MISSING: list[str] = []
ALLOWED_NOT_USED: list[str] = []


def test_no_missing_variables(variables_missing):
    """Test that template variables are declared."""
    assert variables_missing == ALLOWED_MISSING


def test_not_used_variables(variables_not_used):
    """Test that declared variables are used."""
    assert variables_not_used == ALLOWED_NOT_USED
