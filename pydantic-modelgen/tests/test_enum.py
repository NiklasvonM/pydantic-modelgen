import pytest
from pydantic import ValidationError
from pydanticmodelgen import generate_basemodel


def test_enum():
    schema = {
        "type": "object",
        "properties": {"color": {"type": "string", "enum": ["red", "green", "blue"]}},
        "required": ["color"],
    }
    model = generate_basemodel(schema)
    assert model(color="red").color == "red"


def test_enum_wrong():
    schema = {
        "type": "object",
        "properties": {"color": {"type": "string", "enum": ["red", "green", "blue"]}},
        "required": ["color"],
    }
    model = generate_basemodel(schema)
    with pytest.raises(ValidationError):
        model(color="yellow")
