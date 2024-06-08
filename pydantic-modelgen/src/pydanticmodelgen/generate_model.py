from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from typing import Any

from jsonschema import Draft7Validator, validate
from pydantic import BaseModel, Field, create_model


def generate_basemodel(
    schema: Mapping[str, Any], validate_schema: bool = True, model_name: str | None = None
) -> type[BaseModel]:
    """
    Generates a Pydantic BaseModel from a JSON Schema.

    Args:
        schema: The JSON Schema (as a dictionary).
        validate_schema: If True, validates the schema against the JSON Schema specification.
        model_name: Optional name for the generated model. Defaults to 'DynamicModel'

    Raises:
        ValidationError: If `validate_schema` is True and the schema is invalid.

    Returns:
        The generated Pydantic BaseModel class.
    """

    if validate_schema:
        metaschema = Draft7Validator.META_SCHEMA
        validate(schema, metaschema)

    fields: dict[str, Any] = {}
    for prop_name, prop_schema in schema.get("properties", {}).items():
        field_type, field_kwargs = _convert_schema_to_field(prop_name, prop_schema)
        is_required = prop_name in schema.get("required", [])
        field_info = Field(default=... if is_required else None, **field_kwargs)
        fields[prop_name] = (field_type, field_info)

    model_name = model_name or schema.get("title") or "DynamicModel"  # Default model name
    result = create_model(model_name, **fields)
    return result


def _convert_schema_to_field(
    prop_name: str, prop_schema: Mapping[str, Any]
) -> tuple[Any, dict[str, Any]]:
    """
    Converts a JSON Schema property definition to a Pydantic Field type and keyword arguments.

    This function is a placeholder for the actual conversion logic, which would be implemented
    based on the JSON Schema specification (types, formats, constraints, etc.).

    Args:
        prop_name: The name of the JSON Schema property.
        prop_schema: The JSON Schema property definition.

    Returns:
        A tuple containing:
            - The Pydantic Field type (e.g., str, int, float, etc.).
            - A dictionary of keyword arguments for Field (e.g., description, default, etc.).
    """

    # Placeholder implementation:
    field_type = Any  # Default to Any type
    field_kwargs: dict[str, Any] = {}
    if "description" in prop_schema:
        field_kwargs["description"] = prop_schema["description"]
    if "enum" in prop_schema:
        field_type = Enum(prop_name + "Enum", {value: value for value in prop_schema["enum"]})  # type: ignore
    elif "type" in prop_schema:
        type_mapping = {
            "string": str,
            "number": float,
            "integer": int,
            "boolean": bool,
        }
        field_type = type_mapping.get(prop_schema["type"], Any)

        if prop_schema["type"] == "array":
            item_kwargs: dict[str, Any] = {}  # Initialize item_kwargs here
            if "$ref" in prop_schema.get("items", {}):  # Handle references
                item_type = generate_basemodel(prop_schema["items"]["$ref"])
            elif prop_schema["items"].get("type") == "object":
                item_type = generate_basemodel(prop_schema["items"], model_name=prop_name + "Item")
            else:
                item_type, item_kwargs = _convert_schema_to_field(
                    prop_name + "_item", prop_schema.get("items", {})
                )
            return list[item_type], item_kwargs  # type: ignore

        if prop_schema["type"] == "string":
            if prop_schema.get("format") == "date-time":
                field_type = datetime
            else:
                pass

    if "pattern" in prop_schema:
        field_kwargs["pattern"] = prop_schema["pattern"]

    if "exclusiveMinimum" in prop_schema:
        field_kwargs["gt"] = prop_schema["exclusiveMinimum"]
    if "exclusiveMaximum" in prop_schema:
        field_kwargs["lt"] = prop_schema["exclusiveMaximum"]
    if "minimum" in prop_schema:
        field_kwargs["ge"] = prop_schema["minimum"]
    if "maximum" in prop_schema:
        field_kwargs["le"] = prop_schema["maximum"]
    # minLength, maxLength
    if "minLength" in prop_schema:
        field_kwargs["min_length"] = prop_schema["minLength"]
    if "maxLength" in prop_schema:
        field_kwargs["max_length"] = prop_schema["maxLength"]

    # Add logic to handle other schema properties here...

    return field_type, field_kwargs
