from services.general.base_service import BaseService
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.grade_schema import (
    GradeDeleteResponseSchema,
    GradeRequestSchema,
    GradeResponseSchema,
    GradeStatisticResponseSchema,
)
from services.university.models.group_schema import (
    GroupRequestSchema,
    GroupResponseSchema,
)
from services.university.models.student_schema import (
    StudentRequestSchema,
    StudentResponseSchema,
)
from services.university.models.teachers_schema import (
    TeacherRequestSchema,
    TeacherResponseSchema,
)

from utils.api_utils import ApiUtils


class UniversityService(BaseService):
    SERVICE_URL = "http://127.0.0.1:8001"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.group_helper = GroupHelper(self.api_utils)
        self.student_helper = StudentHelper(self.api_utils)
        self.teacher_helper = TeacherHelper(self.api_utils)
        self.grade_helper = GradeHelper(self.api_utils)

    def create_group(self, group_request: GroupRequestSchema) -> GroupResponseSchema:
        response = self.group_helper.post_group(json=group_request.model_dump())
        return GroupResponseSchema(**response.json())

    def create_student(
        self, student_request: StudentRequestSchema
    ) -> StudentResponseSchema:
        response = self.student_helper.post_student(json=student_request.model_dump())
        return StudentResponseSchema(**response.json())

    def create_teacher(
        self, teacher_request: TeacherRequestSchema
    ) -> TeacherResponseSchema:
        response = self.teacher_helper.post_teacher(json=teacher_request.model_dump())
        return TeacherResponseSchema(**response.json())

    def get_teachers(self) -> list[TeacherResponseSchema]:
        response = self.teacher_helper.get_teachers()
        return [TeacherResponseSchema(**teacher) for teacher in response.json()]

    def create_grade(self, grade_request: GradeRequestSchema) -> GradeResponseSchema:
        response = self.grade_helper.post_grade(data=grade_request.model_dump())
        return GradeResponseSchema(**response.json())

    def update_grade(
        self, grade_id: int, grade_request: GradeRequestSchema
    ) -> GradeResponseSchema:
        response = self.grade_helper.put_grade(
            grade_id=grade_id, data=grade_request.model_dump()
        )
        return GradeResponseSchema(**response.json())

    def delete_grade(self, grade_id: int) -> GradeDeleteResponseSchema:
        response = self.grade_helper.delete_grade(grade_id=grade_id)
        return GradeDeleteResponseSchema(**response.json())

    def get_grades(
        self, student_id=None, teacher_id=None, group_id=None
    ) -> list[GradeResponseSchema]:
        response = self.grade_helper.get_grades(
            student_id=student_id,
            teacher_id=teacher_id,
            group_id=group_id,
        )
        return [GradeResponseSchema(**grade) for grade in response.json()]

    def get_grades_stats(
        self, student_id=None, teacher_id=None, group_id=None
    ) -> GradeStatisticResponseSchema:
        response = self.grade_helper.get_grades_stats(
            student_id=student_id,
            teacher_id=teacher_id,
            group_id=group_id,
        )
        return GradeStatisticResponseSchema(**response.json())
