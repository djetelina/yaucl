from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal
from unittest.mock import mock_open, patch

import pytest

from yaucl import BaseConfig, BaseSectionConfig


@dataclass
class SectionTest(BaseSectionConfig):
    """A test section configuration class."""

    section_option: str = "default_section_option"
    section_value: int = 123


@dataclass
class ConfigTest(BaseConfig):
    """A test configuration class."""

    option: str = "default_option"
    value: int = 42
    enabled: bool = True
    literal: Literal["black", "white"] = "black"
    list_of_str: list[str] = field(default_factory=list)
    section: SectionTest = field(default_factory=SectionTest)


@pytest.fixture
def mock_toml_content():
    """Fixture providing mock TOML content."""
    return {
        "option": "toml_option",
        "value": 999,
        "enabled": False,
        "literal": "white",
        "list_of_str": ["a", "b", "c"],
        "section": {"section_option": "toml_section_option", "section_value": 456},
    }

@pytest.fixture
def mock_toml_invalid_types_content():
    return {
        "option": 56,
        "value": "foooooo",
        "enabled": 33,
        "literal": "orange",
        "list_of_str": [1, 2, "c"],
    }

@patch("yaucl.base_config.tomllib.load")
@patch("pathlib.Path.exists")
@patch("pathlib.Path.open", new_callable=mock_open)
def test_toml_loading(mock_file_open, mock_exists, mock_load, mock_toml_content):
    """Test loading configuration from a TOML file."""
    # Mock file exists and TOML content
    mock_exists.return_value = True
    mock_load.return_value = mock_toml_content

    # Create config manually
    config = ConfigTest.init(app_name="test_app", load_from=["toml"], conf_location="/tmp", conf_file_name="test_config.toml")

    config.update_from_toml()

    # Verify the config was updated with TOML values
    assert config.option == mock_toml_content["option"]
    assert config.value == mock_toml_content["value"]
    assert config.enabled is mock_toml_content["enabled"]
    assert config.literal == mock_toml_content["literal"]
    assert config.list_of_str == mock_toml_content["list_of_str"]

    # Verify section was updated
    assert config.section.section_option == mock_toml_content["section"]["section_option"]
    assert config.section.section_value == mock_toml_content["section"]["section_value"]


@patch("yaucl.base_config.tomllib.load")
@patch("pathlib.Path.exists")
@patch("pathlib.Path.open", new_callable=mock_open)
def test_toml_loading_invalid_types(mock_file_open, mock_exists, mock_load, mock_toml_invalid_types_content):
    """Test loading configuration from a TOML file."""
    # Mock file exists and TOML content
    mock_exists.return_value = True
    mock_load.return_value = mock_toml_invalid_types_content

    # Create config manually
    config = ConfigTest.init(app_name="test_app", load_from=["toml"], conf_location="/tmp", conf_file_name="test_config.toml")

    config.update_from_toml()

    # Verify the config was updated with TOML values
    assert config.option == config._defaults["option"]
    assert config.value == config._defaults["value"]
    assert config.enabled is config._defaults["enabled"]
    assert config.literal == config._defaults["literal"]
    assert config.list_of_str == config._defaults["list_of_str"]


@patch("pathlib.Path.exists")
def test_toml_file_not_exists(mock_exists):
    """Test behavior when a TOML file doesn't exist."""
    # Mock file doesn't exist
    mock_exists.return_value = False

    # Create config manually
    config = ConfigTest(_app_name="test_app", _load_from=["toml"], _conf_location="/tmp", _conf_file_name="test_config.toml")

    # Call update_from_toml directly
    config.update_from_toml()

    # Verify config still has default values
    assert config.option == ConfigTest.option
    assert config.value == ConfigTest.value
    assert config.enabled is ConfigTest.enabled
    assert config.section.section_option == SectionTest.section_option
    assert config.section.section_value == SectionTest.section_value


@patch("yaucl.base_config.user_config_path")
def test_conf_file_path(mock_user_config_path):
    """Test determining the configuration file path."""
    # Mock user_config_path
    mock_user_config_path.return_value = Path("/mock/user/config")

    # Test with explicit Path
    config1 = ConfigTest(_app_name="test_app", _load_from=["toml"], _conf_location=Path("/custom/path"), _conf_file_name="test_config.toml")
    assert config1.conf_file_path == Path("/custom/path/test_config.toml")

    # Test with a string path
    config2 = ConfigTest(_app_name="test_app", _load_from=["toml"], _conf_location="/another/path", _conf_file_name="test_config.toml")
    assert config2.conf_file_path == Path("/another/path/test_config.toml")

    # Test with the default path
    config3 = ConfigTest(_app_name="test_app", _load_from=["toml"], _conf_location=None, _conf_file_name="test_config.toml")
    assert config3.conf_file_path == Path("/mock/user/config/test_app/test_config.toml")
