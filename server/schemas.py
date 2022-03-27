from pydantic import BaseModel

class Bottles(BaseModel):
    id: int
    flat: int
    count: int

    class Config:
        orm_mode = True