import pytest
from pydantic import ValidationError
from pydanticmodelgen import generate_basemodel


def test_constraints_in_array() -> None:
    schema = {
        "type": "object",
        "properties": {
            "some_array": {
                "type": "array",
                "items": {"type": "integer", "minimum": 2, "maximum": 3},
            }
        },
    }

    Model = generate_basemodel(schema)
    with pytest.raises(ValidationError):
        Model(some_array=[1])
    with pytest.raises(ValidationError):
        Model(some_array=[1, 2])
    with pytest.raises(ValidationError):
        Model(some_array=[1, 2, 3, 4])
    with pytest.raises(ValidationError):
        Model(some_array=[5])
    assert Model(some_array=[]).some_array == []
    assert Model(some_array=[2, 3]).some_array == [2, 3]
    assert Model(some_array=[2, 3, 2]).some_array == [2, 3, 2]
