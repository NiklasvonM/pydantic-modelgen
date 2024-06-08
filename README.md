# pydantic-modelgen

Create Pydantic `BaseModel`s from JSON Schema at runtime.

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
