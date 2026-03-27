from pydantic import BaseModel

class APIResourceBase(BaseModel):
    name: str
    description: str | None = None
    url: str

class APIResourceCreate(APIResourceBase):
    pass

class APIResourceOut(APIResourceBase):
    id: int
    class Config:
        orm_mode = True
