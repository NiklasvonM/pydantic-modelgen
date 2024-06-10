import pytest
from pydantic import ValidationError
from pydanticmodelgen import generate_basemodel


def test_raises_validation_error() -> None:
    def is_always_false(value: str) -> bool:
        return False

    custom_format = "always_false"
    schema = {
        "type": "object",
        "properties": {"some_value": {"type": "string", "format": custom_format}},
    }

    format_validation = {custom_format: is_always_false}

    Model = generate_basemodel(schema, format_validation=format_validation)
    with pytest.raises(ValidationError):
        Model(some_value="any_value")  # raises pydantic.ValidationError


def test_always_true() -> None:
    def is_always_true(value: str) -> bool:
        return True

    custom_format = "always_true"
    schema = {
        "type": "object",
        "properties": {"some_value": {"type": "string", "format": custom_format}},
    }

    format_validation = {custom_format: is_always_true}

    Model = generate_basemodel(schema, format_validation=format_validation)
    instance = Model(some_value="any_value")
    assert instance.some_value == "any_value"


def test_is_even() -> None:
    def is_even(value: int) -> bool:
        return value % 2 == 0

    custom_format = "even"
    schema = {
        "type": "object",
        "properties": {"even_value": {"type": "integer", "format": custom_format}},
    }

    format_validation = {custom_format: is_even}

    Model = generate_basemodel(schema, format_validation=format_validation)
    instance = Model(even_value=2)
    assert instance.even_value == 2
    with pytest.raises(ValidationError):
        Model(even_value=3)


def test_no_validation() -> None:
    schema = {
        "type": "object",
        "properties": {"some_value": {"type": "integer", "format": "no_validation"}},
    }

    Model = generate_basemodel(schema)
    instance = Model(some_value=2)
    assert instance.some_value == 2


def test_superfluous_validation() -> None:
    schema = {
        "type": "object",
        "properties": {"some_value": {"type": "integer"}},
    }

    Model = generate_basemodel(schema, format_validation={"not_a_format": lambda v: False})
    instance = Model(some_value=2)
    assert instance.some_value == 2
