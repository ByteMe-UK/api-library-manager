from pydantic import BaseModel, HttpUrl, field_validator


class APIResourceBase(BaseModel):
    name: str
    description: str | None = None
    url: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be blank")
        return v.strip()

    @field_validator("url")
    @classmethod
    def url_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("url must not be blank")
        return v.strip()


class APIResourceCreate(APIResourceBase):
    pass


class APIResourceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    url: str | None = None


class APIResourceOut(APIResourceBase):
    id: int

    model_config = {"from_attributes": True}
