import pytest
from pydantic import BaseModel, ValidationError
from pydanticmodelgen import generate_basemodel  # Import your function

BASIC_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "active": {"type": "boolean"},
    },
}

BASIC_SCHEMA_WITH_REQUIRED = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "active": {"type": "boolean"},
    },
    "required": ["name", "age"],
}

SCHEMA_WITH_ENUM = {
    "type": "object",
    "properties": {
        "color": {
            "type": "string",
            "enum": ["red", "green", "blue"],
        },
    },
}

COMPLEX_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "email": {
            "type": "string",
            "format": "email",
        },
        "price": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 100,
        },
        "timestamp": {"type": "string", "format": "date-time"},
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "uniqueItems": True,
        },
    },
    "required": ["id", "email"],
}


NESTED_ARRAY_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "price": {"type": "number"},
                },
                "required": ["name"],
            },
        },
    },
}

SCHEMA_WITH_ALL_TYPES = {
    "type": "object",
    "properties": {
        "string_field": {"type": "string"},
        "number_field": {"type": "number"},
        "integer_field": {"type": "integer"},
        "boolean_field": {"type": "boolean"},
        "null_field": {"type": "null"},
    },
}

SCHEMA_WITH_FORMATS = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "date": {"type": "string", "format": "date"},
        "time": {"type": "string", "format": "time"},
        "uuid": {"type": "string", "format": "uuid"},
    },
}

SCHEMA_WITH_PATTERN = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9_-]{3,16}$",
        },
    },
}

# TODO
SCHEMA_WITH_OBJECT_REF = {
    "type": "object",
    "properties": {
        "person": {"$ref": "#/definitions/Person"},
    },
    "definitions": {
        "Person": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
        },
    },
}

# --- Test Cases ---


def test_basic_model_generation() -> None:
    Model = generate_basemodel(BASIC_SCHEMA)
    fields = Model.model_fields
    assert issubclass(Model, BaseModel)
    assert "name" in fields
    assert "age" in fields
    assert "active" in fields


def test_basic_model_with_required_fields() -> None:
    Model = generate_basemodel(BASIC_SCHEMA_WITH_REQUIRED)
    obj = Model(name="Alice", age=30)
    assert obj.name == "Alice"
    assert obj.age == 30

    with pytest.raises(ValidationError):
        Model(active=True)  # Missing required fields


def test_enum_field_generation() -> None:
    Model = generate_basemodel(SCHEMA_WITH_ENUM)
    obj = Model(color="red")
    assert obj.color == "red"

    with pytest.raises(ValidationError):
        Model(color="yellow")  # Invalid enum value


def test_all_types() -> None:
    # Test generation and validation of a model with all JSON schema types
    Model = generate_basemodel(SCHEMA_WITH_ALL_TYPES)
    obj = Model(
        string_field="test",
        number_field=3.14,
        integer_field=42,
        boolean_field=True,
        null_field=None,
    )
    assert obj.string_field == "test"


def test_formats() -> None:
    Model = generate_basemodel(SCHEMA_WITH_FORMATS)
    obj = Model(email="test@example.com", date="2024-06-08")
    assert obj.email == "test@example.com"


def test_pattern() -> None:
    Model = generate_basemodel(SCHEMA_WITH_PATTERN)
    obj = Model(username="valid_username")
    assert obj.username == "valid_username"

    with pytest.raises(ValidationError):
        Model(username="invalid username")


def test_array_with_objects() -> None:
    Model = generate_basemodel(NESTED_ARRAY_SCHEMA)
    obj = Model(name="test", items=[{"name": "test", "price": 10}])
    assert obj.name == "test"
    assert obj.items[0].name == "test"
    assert obj.items[0].price == 10

    with pytest.raises(ValidationError):
        # Invalid type for price
        Model(name="test", items=[{"name": "test", "price": "ten dollars"}])


def test_complex_schema() -> None:
    Model = generate_basemodel(COMPLEX_SCHEMA)

    with pytest.raises(ValidationError):
        # Missing required fields (id)
        Model(name="test")

    with pytest.raises(ValidationError):
        # Negative price
        Model(id="some_id", email="test@example.com", items=[{"name": "test", "price": -10}])

    with pytest.raises(ValidationError):
        # Zero price
        Model(id="some_id", email="test@example.com", items=[{"name": "test", "price": 0}])

    with pytest.raises(ValidationError):
        # Not enough items in "tags"
        Model(id="some_id", email="test@example.com", tags=[])
