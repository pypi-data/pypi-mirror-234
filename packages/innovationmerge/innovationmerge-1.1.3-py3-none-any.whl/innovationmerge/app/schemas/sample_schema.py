from pydantic import BaseModel


class SampleItem(BaseModel):
    val1: int = 2
    val2: int = 2
