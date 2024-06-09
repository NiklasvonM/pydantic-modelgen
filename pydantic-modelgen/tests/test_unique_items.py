from pydanticmodelgen import generate_basemodel

SCHEMA = {
    "type": "object",
    "properties": {"colors": {"type": "array", "items": {"type": "string"}, "uniqueItems": True}},
}


def test_unique_items() -> None:
    model = generate_basemodel(SCHEMA)
    assert model(colors=["red", "green", "blue"]).colors == {"red", "green", "blue"}


def test_unique_items_wrong() -> None:
    model = generate_basemodel(SCHEMA)
    assert model(colors=["red", "green", "blue", "green"]).colors == {"red", "green", "blue"}
