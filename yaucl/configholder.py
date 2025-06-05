import inspect
import logging
from dataclasses import field
from typing import Any, get_args

from typing_extensions import Self

LOGGER = logging.getLogger(__name__)


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
        return {s: t for s, t in inspect.get_annotations(type(self)).items() if not s.startswith("_")}

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
                self.set_typesafe(key, value)

    def set_typesafe(self, key: str, value: Any) -> None:
        """
        Sets an attribute only if the value is of the correct type.

        Args:
            key: attribute name
            value: value to set
        """
        annotation: type = inspect.get_annotations(type(self))[key]
        validators = [
            type(value) is annotation,
            annotation.__name__ == "Literal" and value in get_args(annotation),
            annotation.__name__ == "list" and all(isinstance(m, get_args(annotation)[0]) for m in value),
        ]
        if any(validators):
            setattr(self, key, value)
        else:
            LOGGER.warning("Couldn't set %s to %s, type mismatch", key, value)
