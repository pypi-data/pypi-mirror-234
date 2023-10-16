"""Testing the client."""

import pytest
from darbia.sns import SandSServices


def test_rejects_invalid_auth() -> None:
    """Test that the client will recognize invalid auth."""
    with pytest.raises(TypeError) as excinfo:
        SandSServices(base_url="", account_number="", token="")
    assert "Account number" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        SandSServices(base_url="", account_number="2", token="")
    assert "Token" in str(excinfo.value)
