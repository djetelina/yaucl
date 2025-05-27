from dataclasses import field
from typing import Any

from typing_extensions import Self


class ConfigHolder:
    """
    Base class for our configuration objects
    """

    _defaults: dict = field(default_factory=dict)

    @property
    def config_options(self) -> dict[str, type]:
        """
        Returns: Configuration options that belong to this section.

        """
        return {s: t for s, t in self.__annotations__.items() if not s.startswith("_")}

    def remember_as_defaults(self) -> None:
        """
        Remembers the current configuration values as the defaults,
        in case the config needs to be reset (e.g., in tests).
        """
        defaults = self.__dict__.copy()
        for k, s in self.sections.items():
            s.remember_as_defaults()
            del defaults[k]
        self._defaults = {k: v for k, v in defaults.items() if not k.startswith("_")}

    def reset(self) -> None:
        """Resets the configuration to its remembered defaults (from `remember_as_defaults`)."""
        for s in self.sections.values():
            s.reset()
        for k, v in self._defaults.items():
            setattr(self, k, v)

    @property
    def sections(self) -> dict[str, Self]:
        """
        Goes through config options and returns configs sections.
        To be considered a section, the class must inherit from `BaseSectionConfig`


        Returns: Config sections instance

        """
        return {s: getattr(self, s) for s, t in self.config_options.items() if isinstance(t, type) and issubclass(t, ConfigHolder)}

    def update_from_dict(self, data: dict[str, Any]) -> None:
        """
        Takes a dict and if any key matches, updates the config.

        Args:
            data: dict with new configuration
        """
        for key, value in data.items():
            if key in self.sections and isinstance(value, dict):
                section = self.sections[key]
                section.update_from_dict(value)
            elif hasattr(self, key):
                setattr(self, key, value)
