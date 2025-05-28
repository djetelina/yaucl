from dataclasses import dataclass, field

from yaucl import BaseConfig, BaseSectionConfig


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


def test_markdown_skeleton():
    desired_doc = """
# Configuring simplebase

## Available options

### General

| Option name | Description | Type | Default |
|--------|-------------|------|---------|
| `option` | -- | `str` | `default_option` |
| `value` | -- | `int` | `42` |
| `enabled` | -- | `bool` | `True` |

### Sections

#### section

| Option name | Description | Type | Default |
|--------|-------------|------|---------|
| `section_option` | -- | `str` | `default_section_option` |
| `section_value` | -- | `int` | `123` |

## Configuration methods

### TOML file

File location:
- Windows: `%APPDATA%/simplebase/config.toml`
- Linux: `~/.config/simplebase/config.toml`
- macOS: `~/Library/Application Support/simplebase/config.toml`

### Environment variables

Environment variables are uppercase option names, with a prefix `SIMPLEBASE_`.
Options outside of General are then prefixed further with the section name."""
    conf = SimpleBaseConfig.init()
    generated_doc = f"{conf.generate_markdown_skeleton()}"
    assert generated_doc == desired_doc
