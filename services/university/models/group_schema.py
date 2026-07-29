import random
from enum import StrEnum

from pydantic import BaseModel


class BaseGroupSchema(BaseModel):
    name: str


class GroupRequestSchema(BaseGroupSchema):
    pass


class GroupResponseSchema(BaseGroupSchema):
    id: int


class Degree(StrEnum):
    ASSOCIATE = "Associate"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORATE = "Doctorate"

    @classmethod
    def random(cls):
        return random.choice(list(cls))
