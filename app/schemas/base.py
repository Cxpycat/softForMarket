from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseInSchema(BaseSchema):
    pass


class BaseOutSchema(BaseSchema):
    id: int
