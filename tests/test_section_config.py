import os
from dataclasses import dataclass, field
from unittest.mock import patch

from yaucl import BaseSectionConfig


@dataclass
class SimpleSection(BaseSectionConfig):
    option: str = "default_option"
    value: int = 42
    enabled: bool = True


@dataclass
class NestedSection(BaseSectionConfig):
    nested_option: str = "nested_default"


@dataclass
class ComplexSection(BaseSectionConfig):
    name: str = "default_name"
    nested: NestedSection = field(default_factory=NestedSection)


def test_section_config_defaults():
    """Test that section config has correct default values."""
    section = SimpleSection()

    assert section.option == SimpleSection.option
    assert section.value == SimpleSection.value
    assert section.enabled is SimpleSection.enabled


def test_update_section_from_dict():
    """Test updating section config from a dictionary."""
    section = SimpleSection()

    section.update_from_dict({"option": "new_option", "value": 100, "enabled": False})

    assert section.option == "new_option"
    assert section.value == 100
    assert section.enabled is False


def test_nested_section_from_dict():
    """Test updating nested section config from a dictionary."""
    section = ComplexSection()

    section.update_from_dict({"name": "new_name", "nested": {"nested_option": "new_nested_option"}})

    assert section.name == "new_name"
    assert section.nested.nested_option == "new_nested_option"


def test_update_from_env():
    """Test updating section config from environment variables."""
    with patch.dict(os.environ, {"APP_SECTION_OPTION": "env_option", "APP_SECTION_VALUE": "100", "APP_SECTION_ENABLED": "false"}):
        section = SimpleSection()
        section.update_from_env("section", prefix=["app"])

        assert section.option == "env_option"
        assert section.value == 100
        assert section.enabled is False


def test_nested_section_from_env():
    """Test updating nested section config from environment variables."""
    with patch.dict(os.environ, {"APP_PARENT_NAME": "env_name", "APP_PARENT_NESTED_NESTED_OPTION": "env_nested_option"}):
        section = ComplexSection()
        section.update_from_env("parent", prefix=["app"])

        assert section.name == "env_name"
        assert section.nested.nested_option == "env_nested_option"
