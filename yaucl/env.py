import logging
import os
from typing import Any, TypeVar, get_args

LOGGER = logging.getLogger(__name__)
T_B = TypeVar("T_B", str, int, float)


def _handle_list(env_value: str, full_annotation: type[list[T_B]]) -> list[T_B] | None:
    provided_list = env_value.split(",")
    list_members_type = get_args(full_annotation)[0]
    try:
        return [list_members_type(m) for m in provided_list]
    except (ValueError, TypeError) as _:
        LOGGER.warning("Unable to parse list from env var %s", env_value)
        return None


def _handle_bool(env_value: str, full_annotation: type[bool]) -> bool:
    return full_annotation(env_value.lower() in ("true", "1", "yes", "y", "t"))


def _handle_literal(env_value: str, full_annotation: type) -> str | int | None:
    if env_value in get_args(full_annotation):
        return env_value
    else:
        LOGGER.warning("Unable to parse literal from env var %s", env_value)
        return None


ADVANCED_HANDLED_TYPES = {
    "list": _handle_list,
    "bool": _handle_bool,
    "Literal": _handle_literal,
}
# The Any in here should be 'Literal', but I can't seem to figure out how to type it
# properly, since Literal seems to be a special cookie
T = TypeVar("T", str, int, float, bool, list, bool, Any)


def get_env_value(name: str, expected_type: type[T]) -> T | None:
    """
    Gets env value and converts it to the expected type.

    Supported types: str, int, float, bool, list, Literal.

    list can be either list[str], list[int] or list[float]

    Literal is expected to have either strings or ints inside

    Any type of failure results in no result

    Args:
        name: name of the env variable, it doesn't need to be uppercase
        expected_type: type the env variable should be converted into
            in case of more complex types, make sure it can be constructed
            from a single string by calling the type: `passed_type(value)`.
            In case of error returns None

    """
    env_var_name = name.upper()
    env_value = os.getenv(env_var_name)

    if env_value is None:
        return None

    try:
        if expected_type.__name__ in ADVANCED_HANDLED_TYPES:
            return ADVANCED_HANDLED_TYPES[expected_type.__name__](env_value, full_annotation=expected_type)
        else:
            return expected_type(env_value)
    except (ValueError, TypeError) as _:
        return None
