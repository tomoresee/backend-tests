from pydantic import BaseModel, Field

from services.university.constants import GradeConstants


class BaseGradeSchema(BaseModel):
    teacher_id: int = Field(gt=0)
    student_id: int = Field(gt=0)
    grade: int = Field(ge=GradeConstants.MIN_GRADE, le=GradeConstants.MAX_GRADE)


class GradeRequestSchema(BaseGradeSchema):
    pass


class GradeResponseSchema(BaseGradeSchema):
    id: int = Field(gt=0)


class GradeDeleteResponseSchema(BaseModel):
    detail: str


class GradeStatisticResponseSchema(BaseModel):
    count: int
    min: int = Field(gt=GradeConstants.MIN_GRADE, description="Минимальная оценка")
    max: int = Field(le=GradeConstants.MAX_GRADE, description="Максимальная оценка")
    avg: float
