from pydantic import BaseModel, Field


class BaseGradeSchema(BaseModel):
    teacher_id: int = Field(gt=0)
    student_id: int = Field(gt=0)
    grade: int = Field(ge=1, le=5)


class GradeRequestSchema(BaseGradeSchema):
    pass


class GradeResponseSchema(BaseGradeSchema):
    id: int = Field(gt=0)


class GradeDeleteResponseSchema(BaseModel):
    detail: str


class GradeStatisticResponseSchema(BaseModel):
    count: int
    min: int
    max: int
    avg: float
