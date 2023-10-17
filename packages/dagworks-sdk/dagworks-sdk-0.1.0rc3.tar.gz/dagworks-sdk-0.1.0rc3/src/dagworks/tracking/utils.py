import dataclasses
import datetime
from enum import Enum
from typing import Union, Any


def make_json_safe(item: Union[dict, list, str, float, int, bool]) -> Any:
    """
    Converts an item to json-serializable format, converting datetime objects to string.

    @param item: A dictionary or list potentially containing non-serializable types.
    @return: A dictionary or list with non-serializable types converted.
    """
    if isinstance(item, dict):
        return {k: make_json_safe(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [make_json_safe(elem) for elem in item]
    elif isinstance(item, datetime.datetime):
        return item.isoformat()  # Convert datetime object to iso format string
    elif dataclasses.is_dataclass(item):
        return make_json_safe(dataclasses.asdict(item))
    elif isinstance(item, Enum):
        return item.value  # Convert enum to its corresponding value
    else:
        return item  # For other types that are json serializable, return as is
