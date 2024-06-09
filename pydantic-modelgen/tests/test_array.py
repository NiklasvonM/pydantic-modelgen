from pydanticmodelgen import generate_basemodel


def test_array_simple():
    schema = {
        "type": "object",
        "properties": {"colors": {"type": "array", "items": {"type": "string"}}},
    }
    model = generate_basemodel(schema)
    assert model(colors=["red", "green"]).colors == ["red", "green"]
