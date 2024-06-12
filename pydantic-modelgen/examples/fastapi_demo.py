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
