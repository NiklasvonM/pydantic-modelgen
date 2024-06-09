import pytest
from pydantic import ValidationError
from pydanticmodelgen import generate_basemodel

SCHEMA = {
    "type": "object",
    "properties": {
        "colors": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
        },
    },
}


def test_min_items() -> None:
    Model = generate_basemodel(SCHEMA)
    assert Model(colors=["red", "green"]).colors == ["red", "green"]


def test_min_items_wrong() -> None:
    Model = generate_basemodel(SCHEMA)
    with pytest.raises(ValidationError):
        Model(colors=["red"])
