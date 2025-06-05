import inspect
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

from yaucl.section_config import BaseSectionConfig

if sys.version_info >= (3, 11):
    from typing import Self

    import tomllib
else:
    import tomli as tomllib
    from typing_extensions import Self

from platformdirs import user_config_path

from yaucl.configholder import ConfigHolder
from yaucl.env import get_env_value

LOGGER = logging.getLogger(__name__)
LOAD_FROM_TYPE = list[Literal["toml", "env"]]


@dataclass
class BaseConfig(ConfigHolder):
    """
    Base class for the root of your configuration. Use it as a dataclass.

    Supported types for configuration values: str, int, float, bool, and `BaseSectionConfig`.

    `BaseSectionConfig` allows you to define another dataclass and use it as a section within the configuration.

    To load the configuration, call the `init` class method. You could use `__init__`, but then you'd
    have to manage some logic by yourself. Try to avoid that.
    """

    _app_name: str | None
    _load_from: LOAD_FROM_TYPE
    _conf_location: str | Path | None
    _conf_file_name: str

    @classmethod
    def init(
        cls,
        app_name: str | None = None,
        load_from: LOAD_FROM_TYPE | None = None,
        conf_location: Path | str | None = None,
        conf_file_name: str = "config.toml",
    ) -> Self:
        """
        Initialization of the Config Class.

        Args:
            app_name: The name of the application.
                Used in default paths and env variables.
            load_from: A list of file types to load configuration from.
                Defaults to ["toml", "env"] if not provided.
                Order matters, rightmost takes precedence.
            conf_location: The location of the configuration file.
                If not provided, location will be determined based on the OS.

                - Windows: `%APPDATA%/<app_name>/`
                - Linux: `~/.config/<app_name>/`
                - macOS: `~/Library/Application Support/<app_name>/`
            conf_file_name: The name of the configuration file.

        Returns:
            Self: Configuration ready to go.
        """
        # For some of these, we don't need properties
        _load_from: LOAD_FROM_TYPE = load_from if load_from is not None else ["toml", "env"]

        self: Self = cls(
            _app_name=app_name,
            _load_from=_load_from,
            _conf_location=conf_location,
            _conf_file_name=conf_file_name,
        )
        self.remember_as_defaults()
        self.load()
        return self

    @property
    def conf_file_path(self) -> Path:
        """
        Gets the configuration file path based on the provided configuration location
        and file name. This property determines the path dynamically by considering
        whether the provided configuration location is a `Path` object or a string,
        or defaults to a user-specific configuration directory if not explicitly set.

        Returns:
            Path: The resolved configuration file path.

        """
        if self._conf_location and isinstance(self._conf_location, Path):
            return self._conf_location / self._conf_file_name
        elif isinstance(self._conf_location, str):
            return Path(self._conf_location) / self._conf_file_name
        else:
            return user_config_path() / self.app_name / self._conf_file_name

    @property
    def app_name(self) -> str:
        """
        Property to retrieve the application name.

        This property attempts to determine the application name automatically if it
        is not explicitly set. If the name cannot be derived from the configuration
        class name, a ValueError is raised. In cases where the name is guessed, a
        warning is logged to indicate potential unpredictability in the deduced name.

        Raises:
            ValueError: If the application name is missing and cannot be guessed.

        Returns:
            str: The name of the application.
        """
        if self._app_name is None:
            guessed_app_name = type(self).__name__.lower().replace("config", "")
            if not guessed_app_name:
                raise ValueError("Please provide an app name, unable to guess it from the config class name.")
            LOGGER.warning(
                "No app name provided, guessed %s from config class name. This might be dangerous.",
                guessed_app_name,
            )
            self._app_name = guessed_app_name
        return self._app_name

    def load(self, reset: bool = False) -> None:
        """
        Loads the data from specified sources and optionally resets before loading. This method loops
        through internal data sources and attempts to invoke corresponding update methods dynamically.
        If no update method is found for a source, a warning is logged.

        Args:
            reset: Whether to reset the current data before loading from the sources. Defaults to False.
        """
        if reset:
            self.reset()
        for source in self._load_from:
            try:
                getattr(self, f"update_from_{source}")()
            except AttributeError:
                LOGGER.warning("No method to update from %s, skipping.", source)

    def update_from_toml(self) -> None:
        """Updates the config from a TOML file."""
        if self.conf_file_path.exists():
            with self.conf_file_path.open("rb") as f:
                config_data = tomllib.load(f)

            self.update_from_dict(config_data)

    def update_from_env(self) -> None:
        """Updates the config from environment variables."""
        for key, expected_type in inspect.get_annotations(type(self)).items():
            if key in self.sections:
                section = getattr(self, key)
                section.update_from_env(key, prefix=[self.app_name])
            else:
                env_value = get_env_value(f"{self.app_name}_{key}", expected_type)
                if env_value is not None:
                    setattr(self, key, env_value)

    def generate_markdown_skeleton(self) -> str:
        """
        Helper function that generates a Markdown skeleton for your documentation.

        Consider adding descriptions to your options, examples, and more.
        """
        doc = f"""
# Configuring {self.app_name}

## Available options

### General

| Option name | Description | Type | Default |
|--------|-------------|------|---------|
"""
        for option, default in self._defaults.items():
            doc += f"""| `{option}` | -- | `{inspect.get_annotations(type(self))[option].__name__}` | `{default}` |\n"""
        if self.sections:
            doc += """\n### Sections\n\n"""
        for section_name, section in self.sections.items():
            section = cast(BaseSectionConfig, section)
            doc += f"#### {section_name}\n{section.generate_markdown_skeleton(section_name)}"
        doc += """\n## Configuration methods\n"""
        for source in self._load_from:
            doc += getattr(self, f"_{source}_doc")
        return doc

    @property
    def _toml_doc(self) -> str:
        doc = f"""
### TOML file

File location:{self._conf_location_all}
"""
        return doc

    @property
    def _conf_location_all(self) -> str:
        if self._conf_location:
            return f"`{self.conf_file_path}`"
        else:
            return f"""
- Windows: `%APPDATA%/{self.app_name}/{self._conf_file_name}`
- Linux: `~/.config/{self.app_name}/{self._conf_file_name}`
- macOS: `~/Library/Application Support/{self.app_name}/{self._conf_file_name}`"""

    @property
    def _env_doc(self):
        doc = f"""
### Environment variables

Environment variables are uppercase option names, with a prefix `{self.app_name.upper()}_`.
"""
        if self.sections:
            doc += """Options outside of General are then prefixed further with the section name."""
        return doc
