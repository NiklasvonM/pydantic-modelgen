from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime, time
from enum import Enum
from typing import Any, List

from dateutil.parser import parse as parse_datetime
from pydantic import BaseModel

from pydanticmodelgen.errors import EnumConversionError


def get_field_type(prop_name: str, prop_schema: Mapping[str, Any]) -> Any:
    """Determines the Pydantic field type from the JSON Schema."""

    schema_type: str | None = prop_schema.get("type")
    schema_format: str | None = prop_schema.get("format")

    field_type = Any
    if "enum" in prop_schema:
        enum_values = prop_schema["enum"]
        try:
            # Convert enum values based on format
            enum_values_converted = {
                enum_value: _load_enum_value(enum_value, prop_schema.get("format"))
                for enum_value in enum_values
            }
            field_type = Enum(prop_name + "Enum", enum_values_converted)  # type: ignore
        except ValueError as e:
            raise EnumConversionError(
                f"Error converting enum values for property '{prop_name}': {e}"
            ) from e
    if schema_format and field_type is Any:
        if schema_format == "date-time":
            field_type = datetime
        elif schema_format == "date":
            field_type = date
        elif schema_format == "time":
            field_type = time
        elif schema_format == "uri":
            field_type = str
        # TODO: Handle other formats that imply a specific type (e.g., email -> str)
    if schema_type and field_type is Any:
        type_mapping = {
            "string": str,
            "number": float,
            "integer": int,
            "boolean": bool,
            "array": List,  # Placeholder, will be replaced in _get_field_kwargs
            "object": BaseModel,  # Placeholder
            "null": None,
        }
        field_type = type_mapping.get(schema_type, Any)

    return field_type


def _load_enum_value(value: str, format: str | None = None) -> Any:
    """Loads an enum value to the appropriate type based on the format."""
    if format == "date-time":
        return parse_datetime(value)
    elif format == "date":
        return parse_datetime(value).date()  # Convert to date object
    else:
        return value
