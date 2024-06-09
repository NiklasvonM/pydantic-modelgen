from collections.abc import Mapping
from typing import Any


def handle_numeric_kwargs(prop_schema: Mapping[str, Any], field_kwargs: dict[str, Any]) -> None:
    """Handles keyword arguments for numeric fields (int, float)."""
    if "exclusiveMinimum" in prop_schema:
        field_kwargs["gt"] = prop_schema["exclusiveMinimum"]
    if "exclusiveMaximum" in prop_schema:
        field_kwargs["lt"] = prop_schema["exclusiveMaximum"]
    if "minimum" in prop_schema:
        field_kwargs["ge"] = prop_schema["minimum"]
    if "maximum" in prop_schema:
        field_kwargs["le"] = prop_schema["maximum"]


def handle_string_kwargs(prop_schema: Mapping[str, Any], field_kwargs: dict[str, Any]) -> None:
    """Handles keyword arguments for string fields."""
    if "pattern" in prop_schema:
        field_kwargs["pattern"] = prop_schema["pattern"]
    if "minLength" in prop_schema:
        field_kwargs["min_length"] = prop_schema["minLength"]
    if "maxLength" in prop_schema:
        field_kwargs["max_length"] = prop_schema["maxLength"]
