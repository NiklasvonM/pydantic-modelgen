from dateutil.parser import parse
from pydanticmodelgen import generate_basemodel


def main() -> None:
    json_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Person Information",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0},
            "birthday": {"format": "date", "enum": ["2000-01-01", "2000-01-02"]},
            "gender": {"enum": ["male", "female", "other"]},
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "country": {"type": "string"},
                },
                "required": ["street", "city"],
            },
            "contact": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "phone": {"type": "string"},
                },
            },
            "friends": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer", "minimum": 0},
                    },
                    "required": ["name"],
                },
                "minItems": 1,
            },
            "price": {"type": "number", "exclusiveMinimum": 0},
        },
        "required": ["name", "age"],
    }

    model = generate_basemodel(json_schema, validate_schema=True)
    print("Model:")
    print(model)
    print("\nModel fields:")
    print(model.model_fields)

    instance = model(
        **{
            "name": "John Doe",
            "age": 30,
            "gender": "male",
            "birthday": parse("2000-01-01").date(),
            "friends": [{"name": "Jane Boe", "age": 25}],
        }
    )
    print("\nInstance:")
    print(instance)


if __name__ == "__main__":
    main()
