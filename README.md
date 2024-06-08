# pydantic-modelgen

Create Pydantic `BaseModel`s from JSON Schema at runtime.

[![Python Version](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Mypy](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/mypy.yml/badge.svg)](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/mypy.yml)
[![Ruff](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/ruff.yml/badge.svg)](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/ruff.yml)
[![Tests](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/tests.yml/badge.svg)](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/tests.yml)
[![Security](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/bandit.yml/badge.svg)](https://github.com/NiklasvonM/pydantic-modelgen/actions/workflows/bandit.yml)

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
# name='John Doe' age=30 gender=<genderEnum.male: 'male'>
```
