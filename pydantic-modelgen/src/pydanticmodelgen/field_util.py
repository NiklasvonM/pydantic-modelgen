from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, List, Set

from pydantic import Field, field_validator


def validation_decorator(validator_func: Callable[[Any], bool], prop_name: str) -> classmethod:
    """Creates a Pydantic validator from a function."""

    def validation_method(cls, value: Any) -> Any:
        if not validator_func(value):
            raise ValueError(f"Invalid value for format in field '{prop_name}': {value}")
        return value

    return field_validator(prop_name)(validation_method)  # type: ignore


def annotate_field_type(field_type: Any, field_info: dict[str, Any]) -> Any:
    """Creates a Pydantic Field with the given type and information."""
    if field_type is List and "item_type" in field_info:
        item_type = field_info.pop("item_type")
        item_field = field_info.pop("item_field", Field())
        item_type = Annotated[item_type, item_field]

        # Pydantic uses `set` for `unique_items`, see
        # https://github.com/pydantic/pydantic-core/issues/296.
        field_type = Set[item_type] if field_info.pop("unique_items", False) else List[item_type]  # type: ignore

    field_type = Annotated[field_type, Field(**field_info)]
    return field_type
