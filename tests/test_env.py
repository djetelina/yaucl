import os
from typing import Literal
from unittest.mock import patch

from yaucl.env import get_env_value


def test_get_env_value_string():
    """Test getting string values from environment variables."""
    with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
        value = get_env_value("TEST_VAR", str)
        assert value == "test_value"

        # Case-insensitive
        value = get_env_value("test_var", str)
        assert value == "test_value"


def test_get_env_value_int():
    """Test getting integer values from environment variables."""
    with patch.dict(os.environ, {"TEST_INT": "42"}):
        value = get_env_value("TEST_INT", int)
        assert value == 42
        assert isinstance(value, int)


def test_get_env_value_float():
    """Test getting float values from environment variables."""
    with patch.dict(os.environ, {"TEST_FLOAT": "3.14"}):
        value = get_env_value("TEST_FLOAT", float)
        assert value == 3.14
        assert isinstance(value, float)


def test_get_env_value_bool():
    """Test getting boolean values from environment variables."""
    # Test truthy values
    for truthy in ["true", "1", "yes", "y", "t"]:
        with patch.dict(os.environ, {"TEST_BOOL": truthy}):
            value = get_env_value("TEST_BOOL", bool)
            assert value is True
            assert isinstance(value, bool)

    # Test falsy values
    for falsy in ["false", "0", "no", "n", "f"]:
        with patch.dict(os.environ, {"TEST_BOOL": falsy}):
            value = get_env_value("TEST_BOOL", bool)
            assert value is False
            assert isinstance(value, bool)


def test_get_env_value_missing():
    """Test behavior when the environment variable is missing."""
    # Ensure the variable doesn't exist
    if "NONEXISTENT_VAR" in os.environ:
        del os.environ["NONEXISTENT_VAR"]

    value = get_env_value("NONEXISTENT_VAR", str)
    assert value is None


def test_get_env_value_invalid_type():
    """Test behavior when the environment variable can't be converted to the expected type."""
    with patch.dict(os.environ, {"TEST_INT": "not_an_int"}):
        value = get_env_value("TEST_INT", int)
        assert value is None

    with patch.dict(os.environ, {"TEST_FLOAT": "not_a_float"}):
        value = get_env_value("TEST_FLOAT", float)
        assert value is None


def test_get_env_value_case_insensitive():
    """Test that environment variable names are case-insensitive."""
    with patch.dict(os.environ, {"TEST_CASE": "value"}):
        # All these should work
        assert get_env_value("TEST_CASE", str) == "value"
        assert get_env_value("test_case", str) == "value"
        assert get_env_value("Test_Case", str) == "value"


def test_get_env_value_list():
    """Test getting list values from environment variables."""
    with patch.dict(os.environ, {"TEST_LIST": "1,2,3"}):
        value = get_env_value("TEST_LIST", list[int])
        assert value == [1, 2, 3]


def test_get_env_value_literal():
    """Test getting literal values from environment variables."""
    with patch.dict(os.environ, {"TEST_LITERAL": "test_value"}):
        value = get_env_value("TEST_LITERAL", Literal["test_value", "another_value"])
        assert value == "test_value"
