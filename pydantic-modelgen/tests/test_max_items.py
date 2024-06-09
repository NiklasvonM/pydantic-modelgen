import pytest
from pydantic import ValidationError
from pydanticmodelgen import generate_basemodel

SCHEMA = {
    "type": "object",
    "properties": {
        "colors": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 3,
        },
    },
}


def test_max_items() -> None:
    Model = generate_basemodel(SCHEMA)
    assert Model(colors=["red", "green", "blue"]).colors == ["red", "green", "blue"]


def test_max_items_wrong() -> None:
    Model = generate_basemodel(SCHEMA)
    with pytest.raises(ValidationError):
        Model(colors=["red", "green", "blue", "yellow"])
