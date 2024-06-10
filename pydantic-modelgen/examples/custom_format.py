"""
This example demonstrates how to use a custom format validation function,
in this case to make sure that an integer is even.
"""

from pydantic import ValidationError
from pydanticmodelgen import generate_basemodel


def main() -> None:
    even_format = "even"
    schema = {
        "type": "object",
        "properties": {"some_value": {"type": "integer", "format": even_format}},
    }

    Model = generate_basemodel(schema, format_validation={even_format: lambda v: value % 2 == 0})
    try:
        value = 0
        Model(some_value=value)
        print(f"`Model(some_value={value})` Ran successfully!")
    except ValidationError:
        raise AssertionError("Should not have raised an error!") from None
    try:
        value = 1
        Model(some_value=value)  # raises pydantic.ValidationError
        raise AssertionError("Should have raised an error!")
    except ValidationError:
        print(f"`Model(some_value={value})` successfully raised an error!")


if __name__ == "__main__":
    main()
