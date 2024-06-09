import pytest
from pydantic import ValidationError
from pydanticmodelgen import generate_basemodel

SCHEMA = {
    "type": "object",
    "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
    "required": ["name"],
}


def test_object() -> None:
    Model = generate_basemodel(SCHEMA)
    assert Model(name="Alice", age=30).name == "Alice"
    assert Model(name="Alice", age=30).age == 30


def test_object_wrong() -> None:
    Model = generate_basemodel(SCHEMA)
    with pytest.raises(ValidationError):
        Model(age=30)
