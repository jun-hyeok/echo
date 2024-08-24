"""Common types used in the Google Sheet API."""
from functools import reduce

DateTimeRenderOption = ["SERIAL_NUMBER", "FORMATTED_STRING"]
Dimension = ["DIMENSION_UNSPECIFIED", "ROWS", "COLUMNS"]
ErrorCode = [
    "ERROR_CODE_UNSPECIFIED",
    "DOCUMENT_TOO_LARGE_TO_EDIT",
    "DOCUMENT_TOO_LARGE_TO_LOAD",
]
InsertDataOption = ["OVERWRITE", "INSERT_ROWS"]
ValueInputOption = ["INPUT_VALUE_OPTION_UNSPECIFIED", "RAW", "USER_ENTERED"]
ValueRenderOption = ["FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"]


def snake_to_camel(any: any):
    """Convert a snake case key or dictionary to camel case key or dictionary."""
    if isinstance(any, dict):
        return snake_to_camel_dict(any)
    elif isinstance(any, tuple):
        return snake_to_camel_tuple(any)
    elif isinstance(any, list):
        return snake_to_camel_list(any)
    elif isinstance(any, str):
        return snake_to_camel_str(any)
    else:
        return any


def camel_to_snake(any: any):
    """Convert a camel case key or dictionary to snake case key or dictionary."""
    if isinstance(any, dict):
        return camel_to_snake_dict(any)
    elif isinstance(any, tuple):
        return camel_to_snake_tuple(any)
    elif isinstance(any, list):
        return camel_to_snake_list(any)
    elif isinstance(any, str):
        return camel_to_snake_str(any)
    else:
        return any


def snake_to_camel_str(name: str):
    """Convert a snake case string to a camel case string."""
    return reduce(lambda a, b: a + b.capitalize(), name.split("_"))


def camel_to_snake_str(name: str):
    """Convert a camel case string to a snake case string."""
    return reduce(lambda a, b: a + ("_" + b if b.isupper() else b), name).lower()


def snake_to_camel_dict(d: dict):
    """Convert a dictionary of snake case keys to camel case keys."""
    return {snake_to_camel_str(k): v for k, v in d.items()}


def camel_to_snake_dict(d: dict):
    """Convert a dictionary of camel case keys to snake case keys."""
    return {camel_to_snake_str(k): v for k, v in d.items()}


def snake_to_camel_tuple(t: tuple):
    """Convert a tuple of snake case keys to camel case keys."""
    return tuple(snake_to_camel_str(k) for k in t)


def camel_to_snake_tuple(t: tuple):
    """Convert a tuple of camel case keys to snake case keys."""
    return tuple(camel_to_snake_str(k) for k in t)


def snake_to_camel_list(l: list):
    """Convert a list of snake case keys to camel case keys."""
    return [snake_to_camel_str(k) for k in l]


def camel_to_snake_list(l: list):
    """Convert a list of camel case keys to snake case keys."""
    return [camel_to_snake_str(k) for k in l]
