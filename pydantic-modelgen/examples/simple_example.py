from pydanticmodelgen import generate_basemodel


def main() -> None:
    json_schema = {
        "title": "Person Information",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0},
            "gender": {"enum": ["male", "female", "other"]},
        },
    }
    model = generate_basemodel(json_schema, validate_schema=True)
    print(model)
    print(model.model_fields)
    instance = model(**{"name": "John Doe", "age": 30, "gender": "male"})
    print(instance)


if __name__ == "__main__":
    main()
