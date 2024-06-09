from pydanticmodelgen import generate_basemodel


def test_additional_properties():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
        "additionalProperties": True,  # Allow any other key-value pairs
    }
    model = generate_basemodel(schema)
    assert model(name="Alice", age=30).age == 30
