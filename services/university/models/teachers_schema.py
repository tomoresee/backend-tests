import random

from pydantic import BaseModel
from enum import StrEnum


class BaseTeacherSchema(BaseModel):
    first_name: str
    last_name: str
    subject: str


class TeacherRequestSchema(BaseTeacherSchema):
    pass


class TeacherResponseSchema(BaseTeacherSchema):
    id: int


class Subject(StrEnum):
    MATHEMATICS = "Mathematics"
    PHYSICS = "Physics"
    HISTORY = "History"
    BIOLOGY = "Biology"
    GEOGRAPHY = "Geography"

    @classmethod
    def random(cls):
        return random.choice(list(cls))
