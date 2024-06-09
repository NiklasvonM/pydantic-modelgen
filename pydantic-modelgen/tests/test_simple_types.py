from pydantic import BaseModel
from pydanticmodelgen import generate_basemodel


def test_string_type() -> None:
    schema = {"type": "string"}
    Model = generate_basemodel(schema)
    assert issubclass(Model, BaseModel)


def test_integer_type() -> None:
    schema = {"type": "integer"}
    Model = generate_basemodel(schema)
    assert issubclass(Model, BaseModel)


def test_number_type() -> None:
    schema = {"type": "number"}
    Model = generate_basemodel(schema)
    assert issubclass(Model, BaseModel)


def test_boolean_type() -> None:
    schema = {"type": "boolean"}
    Model = generate_basemodel(schema)
    assert issubclass(Model, BaseModel)
