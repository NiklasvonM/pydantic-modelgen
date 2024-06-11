from collections.abc import Mapping
from typing import Any


def handle_numeric_kwargs(prop_schema: Mapping[str, Any], field_kwargs: dict[str, Any]) -> None:
    """
    Handles keyword arguments for numeric fields (int, float).

    Supports
    - exclusiveMinimum
    - exclusiveMaximum
    - minimum
    - maximum

    :param prop_schema: The JSON Schema for the property.
    :param field_kwargs: The keyword arguments for the Pydantic Field to which the options will be
        added.
    :return: None

    """
    if "exclusiveMinimum" in prop_schema:
        field_kwargs["gt"] = prop_schema["exclusiveMinimum"]
    if "exclusiveMaximum" in prop_schema:
        field_kwargs["lt"] = prop_schema["exclusiveMaximum"]
    if "minimum" in prop_schema:
        field_kwargs["ge"] = prop_schema["minimum"]
    if "maximum" in prop_schema:
        field_kwargs["le"] = prop_schema["maximum"]


def handle_string_kwargs(prop_schema: Mapping[str, Any], field_kwargs: dict[str, Any]) -> None:
    """
    Handles keyword arguments for string fields.

    Supports
    - pattern
    - minLength
    - maxLength

    :param prop_schema: The JSON Schema for the property.
    :param field_kwargs: The keyword arguments for the Pydantic Field to which the options will be
        added.
    :return: None
    """
    if "pattern" in prop_schema:
        field_kwargs["pattern"] = prop_schema["pattern"]
    if "minLength" in prop_schema:
        field_kwargs["min_length"] = prop_schema["minLength"]
    if "maxLength" in prop_schema:
        field_kwargs["max_length"] = prop_schema["maxLength"]


def handle_array_kwargs(prop_schema: Mapping[str, Any], field_kwargs: dict[str, Any]) -> None:
    if "minItems" in prop_schema:
        field_kwargs["min_length"] = prop_schema["minItems"]
    if "maxItems" in prop_schema:
        field_kwargs["max_length"] = prop_schema["maxItems"]
    if "uniqueItems" in prop_schema:
        # Pydantic doesn't support `unique_items` as a keyword argument,
        # but we use `Set` instead of `List` later on when calling `pydantic.Field`.
        field_kwargs["unique_items"] = prop_schema["uniqueItems"]
