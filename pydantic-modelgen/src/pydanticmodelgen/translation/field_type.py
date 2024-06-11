from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime, time
from enum import Enum
from typing import Any, List
from uuid import UUID

from dateutil.parser import parse as parse_datetime
from pydantic import BaseModel

from pydanticmodelgen.errors import EnumConversionError


def get_field_type(prop_name: str, prop_schema: Mapping[str, Any]) -> Any:
    """Determines the Pydantic field type from the JSON Schema."""
    if "enum" in prop_schema:
        return create_enum_type(prop_name, prop_schema)
    return map_schema_to_field_type(prop_schema)


def create_enum_type(prop_name: str, prop_schema: Mapping[str, Any]) -> Enum:
    """
    Creates an Enum type (class) from the JSON Schema's 'enum' property.

    :param prop_name: The name of the property, used in the Enum name.
    :param prop_schema: The JSON Schema for the property.
    :return: The Enum type.
    """
    enum_values = prop_schema["enum"]
    try:
        enum_members = {
            enum_value: load_enum_value(enum_value, prop_schema.get("format"))
            for enum_value in enum_values
        }
        return Enum(prop_name + "Enum", enum_members)  # type: ignore
    except ValueError as e:
        raise EnumConversionError(
            f"Error converting enum values for property '{prop_name}': {e}"
        ) from e


def map_schema_to_field_type(prop_schema: Mapping[str, Any]) -> Any:
    """
    Maps JSON Schema type or format to the corresponding Pydantic field type.
    The format takes precedence over the type.
    If neither a type nor a format is specified, `Any` is returned.

    :param prop_schema: The JSON Schema for the property.
    :return: The corresponding field type, for example `str` or `datetime`.
    """
    field_type = map_schema_type_to_base_type(prop_schema)
    field_type = map_schema_format_to_field_type(prop_schema, field_type)
    return field_type


def map_schema_type_to_base_type(prop_schema: Mapping[str, Any]) -> Any:
    """Maps the JSON Schema type to a base Python type."""
    type_mapping: dict[str, Any] = {
        "string": str,
        "number": float,
        "integer": int,
        "boolean": bool,
        "array": List,  # Placeholder, will be replaced elsewhere
        "object": BaseModel,  # Placeholder
        "null": None,
    }
    return type_mapping.get(str(prop_schema.get("type")), Any)


def map_schema_format_to_field_type(prop_schema: Mapping[str, Any], base_type: Any = Any) -> Any:
    """
    Maps the JSON Schema format to a specific field type, using the base type as a default.

    Supports
    - date-time
    - time
    - date
    - duration
    - email
    - idn-email
    - hostname
    - idn-hostname
    - ipv4
    - ipv6
    - uuid
    - uri
    - uri-reference
    - uri-template
    - iri
    - iri-reference
    - iri-template
    - json-pointer
    - relative-json-pointer
    - regex

    most of which simply map to `str`.

    :param prop_schema: JSON Schema of the current property
    :param base_type: Optional default value to use if the format is not supported.
    :return: The mapped field type, which, in most cases, is `str`.
    """
    format_mapping: dict[str, Any] = {
        "date-time": datetime,
        "time": time,
        "date": date,
        "duration": str,
        "email": str,
        "idn-email": str,
        "hostname": str,
        "idn-hostname": str,
        "ipv4": str,
        "ipv6": str,
        "uuid": UUID,
        "uri": str,
        "uri-reference": str,
        "uri-template": str,
        "iri": str,
        "iri-reference": str,
        "iri-template": str,
        "json-pointer": str,
        "relative-json-pointer": str,
        "regex": str,
    }
    return format_mapping.get(str(prop_schema.get("format")), base_type)


def load_enum_value(value: str, format: str | None = None) -> Any:
    """Loads an enum value to the appropriate type based on the format."""
    if format == "date-time":
        return parse_datetime(value)
    if format == "date":
        return parse_datetime(value).date()
    if format == "time":
        return parse_datetime(value).time()
    return value
