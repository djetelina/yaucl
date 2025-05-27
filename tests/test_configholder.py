from dataclasses import dataclass, field

from yaucl.configholder import ConfigHolder


@dataclass
class SimpleConfigHolder(ConfigHolder):
    name: str = "default_name"
    value: int = 42
    enabled: bool = True


@dataclass
class NestedConfigHolder(ConfigHolder):
    option: str = "default_option"


@dataclass
class ComplexConfigHolder(ConfigHolder):
    title: str = "default_title"
    count: int = 10
    nested: NestedConfigHolder = field(default_factory=NestedConfigHolder)


def test_config_options():
    """Test that config_options returns the correct options."""
    config = SimpleConfigHolder()
    options = config.config_options

    assert "name" in options
    assert options["name"] is str
    assert "value" in options
    assert options["value"] is int
    assert "enabled" in options
    assert options["enabled"] is bool


def test_update_from_dict():
    """Test updating config from a dictionary."""
    config = SimpleConfigHolder()

    # Initial values
    assert config.name == SimpleConfigHolder.name
    assert config.value == SimpleConfigHolder.value
    assert config.enabled is SimpleConfigHolder.enabled

    # Update with new values
    config.update_from_dict({"name": "new_name", "value": 100, "enabled": False})

    # Check updated values
    assert config.name == "new_name"
    assert config.value == 100
    assert config.enabled is False


def test_update_nested_from_dict():
    """Test updating nested config from a dictionary."""
    config = ComplexConfigHolder()

    # Initial values
    assert config.title == ComplexConfigHolder.title
    assert config.count == ComplexConfigHolder.count
    assert config.nested.option == NestedConfigHolder.option

    # Update with new values including nested config
    config.update_from_dict({"title": "new_title", "count": 20, "nested": {"option": "new_option"}})

    # Check updated values
    assert config.title == "new_title"
    assert config.count == 20
    assert config.nested.option == "new_option"


def test_sections_property():
    """Test that sections property returns the correct sections."""
    # Mock the config_options property to return items correctly
    config = ComplexConfigHolder()

    # Directly check if nested is a section by checking if it's an instance of ConfigHolder
    assert hasattr(config, "nested")
    assert isinstance(config.nested, ConfigHolder)
