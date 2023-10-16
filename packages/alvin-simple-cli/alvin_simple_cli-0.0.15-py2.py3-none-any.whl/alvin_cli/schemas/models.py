from humps import camelize
from pydantic import BaseModel


def to_camel(s: str) -> str:
    return camelize(s)


class CamelBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True

