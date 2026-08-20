from faker import Faker

from logger.logger import Logger
from services.university.constants import GradeConstants, GradeDefaultCountsConstants
from services.university.models.grade_schema import GradeRequestSchema, GradeStatisticResponseSchema

fake = Faker()


class TestDataHelper:

    @staticmethod
    def create_multiple_grades(grade_admin, teacher_id, student_id, count=None):
        """
        Создает несколько случайных оценок для теста
        """
        if count is None:
            count = fake.random_int(GradeDefaultCountsConstants.DEFAULT_COUNT_MIN,
                                    GradeDefaultCountsConstants.DEFAULT_COUNT_MAX)

        created_grades = []

        for _ in range(count):
            grade_value = fake.random_int(GradeConstants.MIN_GRADE, GradeConstants.MAX_GRADE)
            created_grade = grade_admin.create_grade(
                GradeRequestSchema(
                    teacher_id=teacher_id, student_id=student_id, grade=grade_value
                )
            )
            created_grades.append(created_grade)
            Logger.info(f"Создана оценка: {grade_value} (ID: {created_grade.id})")

        Logger.info(f"Всего создано {count} оценок")
        return created_grades

    @staticmethod
    def calculate_grades_stats(grades):
        """
        Рассчитывает статистику по списку оценок
        """
        if not grades:
            return GradeStatisticResponseSchema(
                count=0,
                min=None,
                max=None,
                avg=None
            )

        grades_values = [g.grade for g in grades]

        return GradeStatisticResponseSchema(
            count=len(grades_values),
            min=min(grades_values),
            max=max(grades_values),
            avg=sum(grades_values) / len(grades_values)
        )
