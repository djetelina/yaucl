import os
from dataclasses import dataclass, field
from unittest.mock import patch

from yaucl import BaseConfig, BaseSectionConfig


@dataclass
class SectionTest(BaseSectionConfig):
    """A test section configuration class."""

    section_option: str = "default_section_option"
    section_value: int = 123
    section_enabled: bool = True


@dataclass
class ConfigTest(BaseConfig):
    """A test configuration class."""

    option: str = "default_option"
    value: int = 42
    enabled: bool = True
    section: SectionTest = field(default_factory=SectionTest)


def test_env_variables_basic():
    """Test basic environment variable handling."""
    with patch.dict(os.environ, {"TEST_OPTION": "env_option", "TEST_VALUE": "100", "TEST_ENABLED": "false"}):
        # Create config manually
        config = ConfigTest(
            _app_name="test",
            _load_from=[],  # Empty to avoid automatic loading
            _conf_location="/tmp",
            _conf_file_name="test_config.toml",
        )

        config.update_from_env()

        # Verify config was updated with environment values
        assert config.option == "env_option"
        assert config.value == 100
        assert config.enabled is False


def test_env_variables_nested():
    """Test environment variable handling for nested sections."""
    with patch.dict(
        os.environ,
        {"TEST_SECTION_SECTION_OPTION": "env_section_option", "TEST_SECTION_SECTION_VALUE": "456", "TEST_SECTION_SECTION_ENABLED": "false"},
    ):
        # Create config manually
        config = ConfigTest(
            _app_name="test",
            _load_from=[],  # Empty to avoid automatic loading
            _conf_location="/tmp",
            _conf_file_name="test_config.toml",
        )

        config.update_from_env()

        # Verify section was updated with environment values
        assert config.section.section_option == "env_section_option"
        assert config.section.section_value == 456
        assert config.section.section_enabled is False


def test_env_variables_mixed():
    """Test environment variable handling with mixed values."""
    with patch.dict(os.environ, {"TEST_OPTION": "env_option", "TEST_SECTION_SECTION_OPTION": "env_section_option"}):
        # Create config manually
        config = ConfigTest(
            _app_name="test",
            _load_from=[],  # Empty to avoid automatic loading
            _conf_location="/tmp",
            _conf_file_name="test_config.toml",
        )

        config.update_from_env()

        # Verify config was updated with environment values
        assert config.option == "env_option"
        assert config.value == 42  # Default, not in environment
        assert config.enabled is True  # Default, not in environment
        assert config.section.section_option == "env_section_option"
        assert config.section.section_value == 123  # Default, not in environment
        assert config.section.section_enabled is True  # Default, not in environment
