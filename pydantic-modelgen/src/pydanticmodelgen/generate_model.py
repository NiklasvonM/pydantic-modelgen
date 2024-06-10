from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Annotated, Any, List, Set, cast

from jsonschema import Draft7Validator, validate
from pydantic import BaseModel, ConfigDict, Field, create_model, field_validator

from .translation import get_field_type, handle_numeric_kwargs, handle_string_kwargs


def generate_basemodel(
    schema: Mapping[str, Any],
    validate_schema: bool = True,
    model_name: str | None = None,
    format_validation: Mapping[str, Callable[[Any], bool]] | None = None,
) -> type[BaseModel]:
    """
    Generates a Pydantic BaseModel from a JSON Schema.

    :param schema: The JSON Schema to convert to a Pydantic model.
    :param validate_schema: Whether to validate the JSON Schema. Defaults to True.
    :param model_name: The name of the model. If not provided, uses the title of the schema or
        "DynamicModel".
    :param format_validation: A mapping of custom format names to validation functions.
        The functions are assumed to take the value and return whether or not they are valid based
        on the format.
    :return: The generated Pydantic BaseModel.
    """

    if validate_schema:
        validate(schema, Draft7Validator.META_SCHEMA)

    fields, validators = create_fields_and_validators_from_schema(
        schema, format_validation=format_validation
    )
    model_name = model_name or schema.get("title") or "DynamicModel"  # Default model name
    config_dict = ConfigDict(
        extra="allow" if schema.get("additionalProperties", False) else "ignore",
        use_enum_values=True,
    )
    result = create_model(model_name, __config__=config_dict, __validators__=validators, **fields)
    return result


def create_fields_and_validators_from_schema(
    schema: Mapping[str, Any],
    format_validation: Mapping[str, Callable[[Any], bool]] | None = None,
) -> tuple[dict[str, Any], dict[str, classmethod]]:
    fields: dict[str, Any] = {}
    validators: dict[str, classmethod] = {}
    properties: dict[str, dict[str, Any]] = schema.get("properties", {})
    for prop_name, prop_schema in properties.items():
        required = prop_name in schema.get("required", [])
        field, validator = create_field_and_validator_from_properties(
            prop_name, prop_schema, required=required, format_validation=format_validation
        )
        fields[prop_name] = field
        if validator is not None:
            validators[prop_name + "_validator"] = validator
    return fields, validators


def create_field_and_validator_from_properties(
    prop_name: str,
    prop_schema: Mapping[str, Any],
    required: bool,
    format_validation: Mapping[str, Callable[[Any], bool]] | None = None,
) -> tuple[Any, classmethod | None]:
    field_type = get_field_type(prop_name, prop_schema)

    field_kwargs = get_field_kwargs(prop_name, prop_schema, field_type)
    default_value = prop_schema.get("default")
    field_info = {"default": ... if required else default_value, **field_kwargs}
    field = annotate_field_type(field_type, field_info)

    validator = None
    if format_validation and "format" in prop_schema:
        format_name = prop_schema["format"]
        if format_name in format_validation:
            validator = validation_decorator(format_validation[format_name], prop_name)

    return field, validator


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

        # Pydantic uses `set` for `unique_items`, see
        # https://github.com/pydantic/pydantic-core/issues/296.
        field_type = Set[item_type] if field_info.pop("unique_items", False) else List[item_type]  # type: ignore

    field_type = Annotated[field_type, Field(**field_info)]
    return field_type


def get_field_kwargs(
    prop_name: str, prop_schema: Mapping[str, Any], field_type: Any
) -> dict[str, Any]:
    """Generates keyword arguments for the Pydantic Field."""

    field_kwargs: dict[str, Any] = {}
    if "description" in prop_schema:
        field_kwargs["description"] = prop_schema["description"]
    if field_type in [int, float]:
        handle_numeric_kwargs(prop_schema, field_kwargs)
    if field_type is str:
        handle_string_kwargs(prop_schema, field_kwargs)
    if field_type is List:
        handle_array_kwargs(prop_name, prop_schema, field_kwargs)

    return field_kwargs


def handle_array_kwargs(
    prop_name: str, prop_schema: Mapping[str, Any], field_kwargs: dict[str, Any]
) -> None:
    if "minItems" in prop_schema:
        field_kwargs["min_length"] = prop_schema["minItems"]
    if "maxItems" in prop_schema:
        field_kwargs["max_length"] = prop_schema["maxItems"]
    if "uniqueItems" in prop_schema:
        # Pydantic doesn't support `unique_items` as a keyword argument,
        # but we use `Set` instead of `List` later on when calling `pydantic.Field`.
        field_kwargs["unique_items"] = prop_schema["uniqueItems"]

    # Get array item type and additional field parameters for items
    item_type, item_field_kwargs = get_field_type_and_kwargs_for_array_items(
        prop_name + "_item", cast(Mapping[str, Any], prop_schema.get("items", {}))
    )
    field_kwargs["item_type"] = item_type
    if item_field_kwargs:
        field_kwargs["item_field"] = Field(**item_field_kwargs)


def get_field_type_and_kwargs_for_array_items(prop_name: str, prop_schema: Mapping[str, Any]):
    if "$ref" in prop_schema:
        item_type = generate_basemodel(prop_schema["$ref"], validate_schema=False)
        return item_type, {}
    elif prop_schema.get("type") == "object":
        item_type = generate_basemodel(prop_schema, model_name=prop_name + "Item")
        return item_type, {}
    else:
        item_type = get_field_type(prop_name, prop_schema)
        item_field_kwargs = get_field_kwargs(prop_name, prop_schema, item_type)
        return item_type, item_field_kwargs
