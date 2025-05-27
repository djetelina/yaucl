import os
from dataclasses import dataclass, field
from pathlib import Path
from unittest.mock import mock_open, patch

from yaucl import BaseConfig, BaseSectionConfig


@dataclass
class SectionConfigTest(BaseSectionConfig):
    section_option: str = "default_section_option"
    section_value: int = 123


@dataclass
class ConfigTest(BaseConfig):
    option: str = "default_option"
    value: int = 42
    enabled: bool = True
    section: SectionConfigTest = field(default_factory=SectionConfigTest)


def test_init_with_defaults():
    """Test initializing BaseConfig with default values."""
    config = ConfigTest.init()

    # Check default values
    assert config.option == "default_option"
    assert config.value == 42
    assert config.enabled is True
    assert config.section.section_option == "default_section_option"
    assert config.section.section_value == 123

    # Check internal values
    assert config._load_from == ["toml", "env"]
    assert config._conf_file_name == "config.toml"


def test_init_with_custom_values():
    """Test initializing BaseConfig with custom values."""
    config = ConfigTest.init(app_name="custom_app", load_from=["env"], conf_location="/tmp", conf_file_name="custom_config.toml")

    # Check internal values
    assert config._app_name == "custom_app"
    assert config._load_from == ["env"]
    assert config._conf_location == "/tmp"
    assert config._conf_file_name == "custom_config.toml"


def test_app_name_guessing():
    """Test that app_name is guessed from the class name if not provided."""
    config = ConfigTest.init()

    # App name should be guessed from TestConfig -> test
    assert config.app_name == "test"


def test_conf_file_path():
    """Test that conf_file_path is correctly determined."""
    # Test with a Path object
    config1 = ConfigTest.init(conf_location=Path("/tmp"))
    assert config1.conf_file_path == Path("/tmp/config.toml")

    # Test with string
    config2 = ConfigTest.init(conf_location="/var/tmp")
    assert config2.conf_file_path == Path("/var/tmp/config.toml")


@patch("yaucl.base_config.tomllib.load")
@patch("pathlib.Path.exists")
@patch("pathlib.Path.open", new_callable=mock_open)
def test_update_from_toml(mock_file_open, mock_exists, mock_load):
    """Test updating config from a TOML file."""
    # Mock file exists and TOML content
    mock_exists.return_value = True
    mock_load.return_value = {"option": "toml_option", "value": 999, "section": {"section_option": "toml_section_option"}}

    config = ConfigTest.init(app_name="test_app", load_from=["toml"])

    # Check values were updated from TOML
    assert config.option == "toml_option"
    assert config.value == 999
    assert config.section.section_option == "toml_section_option"
    # This value wasn't in the TOML, so it should remain default
    assert config.section.section_value == 123


@patch.dict(
    os.environ, {"TEST_OPTION": "env_option", "TEST_VALUE": "888", "TEST_ENABLED": "false", "TEST_SECTION_SECTION_OPTION": "env_section_option"}
)
def test_update_from_env():
    """Test updating config from environment variables."""
    config = ConfigTest.init(app_name="test", load_from=["env"])

    # Check values were updated from environment
    assert config.option == "env_option"
    assert config.value == 888
    assert config.enabled is False
    assert config.section.section_option == "env_section_option"


def test_load_order():
    """Test that load order is respected (rightmost takes precedence)."""
    with patch.dict(os.environ, {"TEST_OPTION": "env_option", "TEST_VALUE": "888"}):
        with patch("yaucl.base_config.tomllib.load") as mock_load:
            with patch("pathlib.Path.exists") as mock_exists:
                with patch("pathlib.Path.open", new_callable=mock_open):
                    # Mock TOML file exists and content
                    mock_exists.return_value = True
                    mock_load.return_value = {"option": "toml_option", "value": 999}

                    # Load from TOML then ENV - ENV should take precedence
                    config1 = ConfigTest.init(app_name="test", load_from=["toml", "env"])
                    assert config1.option == "env_option"
                    assert config1.value == 888

                    # Load from ENV then TOML - TOML should take precedence
                    config2 = ConfigTest.init(app_name="test", load_from=["env", "toml"])
                    assert config2.option == "toml_option"
                    assert config2.value == 999


def test_reset():
    with patch.dict(os.environ, {"TEST_OPTION": "env_option", "TEST_VALUE": "888"}):
        config = ConfigTest.init(app_name="test", load_from=["env"])
        config.reset()
        assert config.option == "default_option"
        assert config.value == 42
