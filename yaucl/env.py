import os
from typing import TypeVar

T = TypeVar("T", str, int, float, bool)


def get_env_value(name: str, expected_type: type[T]) -> T | None:
    """
    Gets env value and converts it to the expected type.

    # TODO lists maybe?

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
        if expected_type is bool:
            return expected_type(env_value.lower() in ("true", "1", "yes", "y", "t"))
        return expected_type(env_value)
    except (ValueError, TypeError) as _:
        return None
