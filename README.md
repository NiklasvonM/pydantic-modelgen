# pydantic-modelgen

Create Pydantic `BaseModel`s from JSON Schema at runtime.

[![Python Version](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Mypy](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/mypy.yml/badge.svg)](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/mypy.yml)
[![Ruff](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/ruff.yml/badge.svg)](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/ruff.yml)
[![Tests](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/tests.yml/badge.svg)](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/tests.yml)
[![Security](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/bandit.yml/badge.svg)](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/bandit.yml)

See [documentation](https://niklasvonm.github.io/pydantic-modelgen/).

## Usage

```python
from pydanticmodelgen import generate_basemodel

json_schema = {
    "title": "Person Information",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
        "gender": {"enum": ["male", "female", "other"]}
    }
}
model = generate_basemodel(json_schema, validate_schema=True)
print(model)
# <class 'pydanticmodelgen.generate_model.Person Information'>
print(model.model_fields)
# {'name': FieldInfo(annotation=str, required=False, default=None), 'age': FieldInfo(annotation=int, required=False, default=None, metadata=[Ge(ge=0)]), 'gender': FieldInfo(annotation=genderEnum, required=False, default=None)}
instance = model(**{"name": "John Doe", "age": 30, "gender": "male"})
print(instance)
# name='John Doe' age=30 gender='male'
```

## Motivation

The motivation for this project is to create dynamic Swagger API documentations for FastAPI apps, which rely on Pydantic, from JSON Schema. This is useful when the application logic does not depend on the exact schema of the JSON, but the consumers of the REST API do. For example, this may be the case if the JSON is populated via an LLM.

If data validation is your only concern, [python-jsonschema](https://github.com/python-jsonschema/jsonschema) is recommended.

<details open>
    <summary>Demo FastAPI App</summary>

```python
import uvicorn
from fastapi import FastAPI
from pydanticmodelgen import generate_basemodel

app = FastAPI(title="Pydantic Modelgen Demo")

json_schema = {
    "title": "Person Information",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
        "gender": {"enum": ["male", "female", "other"]},
    },
}

Model = generate_basemodel(json_schema)

@app.get("/", response_model=Model)
async def root():
    return Model(name="Alice", age=30)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

</details>

While running this FastAPI app, the following documentation can be accessed under localhost:8000/docs:

![Swagger API Documentation](docs/Swagger%20Documentation%20Demo.png)
