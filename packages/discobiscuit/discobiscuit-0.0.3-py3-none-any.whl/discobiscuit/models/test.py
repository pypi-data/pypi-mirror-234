from pydantic import BaseModel

class TestModel(BaseModel):
    name: str
    length: int