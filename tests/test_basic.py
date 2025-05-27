import os
from dataclasses import dataclass, field
from unittest.mock import patch


from yaucl.configholder import ConfigHolder
from yaucl.env import get_env_value
from yaucl import BaseConfig, BaseSectionConfig


@dataclass
class SimpleConfig(ConfigHolder):
    """A simple configuration class for testing."""

    name: str = "default_name"
    value: int = 42
    enabled: bool = True


@dataclass
class SimpleSection(BaseSectionConfig):
    """A simple section configuration class for testing."""

    section_option: str = "default_section_option"
    section_value: int = 123


@dataclass
class SimpleBaseConfig(BaseConfig):
    """A simple base configuration class for testing."""

    option: str = "default_option"
    value: int = 42
    enabled: bool = True
    section: SimpleSection = field(default_factory=SimpleSection)


def test_config_attributes():
    """Test that configuration attributes are accessible."""
    config = SimpleConfig()

    assert config.name == "default_name"
    assert config.value == 42
    assert config.enabled is True


def test_manual_update():
    """Test manually updating configuration values."""
    config = SimpleConfig()

    config.name = "new_name"
    config.value = 100
    config.enabled = False

    assert config.name == "new_name"
    assert config.value == 100
    assert config.enabled is False


def test_env_get_value():
    """Test getting values from environment variables."""
    with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
        value = get_env_value("TEST_VAR", str)
        assert value == "test_value"

    with patch.dict(os.environ, {"TEST_INT": "42"}):
        value = get_env_value("TEST_INT", int)
        assert value == 42
        assert isinstance(value, int)

    with patch.dict(os.environ, {"TEST_FLOAT": "3.14"}):
        value = get_env_value("TEST_FLOAT", float)
        assert value == 3.14
        assert isinstance(value, float)

    with patch.dict(os.environ, {"TEST_BOOL": "true"}):
        value = get_env_value("TEST_BOOL", bool)
        assert value is True
        assert isinstance(value, bool)


def test_section_attributes():
    """Test that section configuration attributes are accessible."""
    section = SimpleSection()

    assert section.section_option == SimpleSection.section_option
    assert section.section_value == SimpleSection.section_value


def test_base_config_init():
    """Test initializing a base configuration with custom values."""
    # We'll manually create and set up the config to avoid using the init method
    config = SimpleBaseConfig(_app_name="test_app", _load_from=["env"], _conf_location="/tmp", _conf_file_name="test_config.toml")

    assert config._app_name == "test_app"
    assert config._load_from == ["env"]
    assert config._conf_location == "/tmp"
    assert config._conf_file_name == "test_config.toml"

    # Check default values
    assert config.option == SimpleBaseConfig.option
    assert config.value == SimpleBaseConfig.value
    assert config.enabled is SimpleBaseConfig.enabled
    assert config.section.section_option == SimpleSection.section_option
    assert config.section.section_value == SimpleSection.section_value
