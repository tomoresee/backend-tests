from pydantic import BaseModel


class BaseStudentSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    degree: str
    phone: str
    group_id: int


class StudentRequestSchema(BaseStudentSchema):
    pass


class StudentResponseSchema(BaseStudentSchema):
    id: int
