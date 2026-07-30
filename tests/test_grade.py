from faker import Faker

from logger.logger import Logger
from services.university.helpers.test_data_helpers import TestDataHelper
from services.university.models.grade_schema import GradeRequestSchema
from services.university.university_service import UniversityService

fake = Faker()


class TestGrade:
    def test_create_grade(
            self, university_api_utils_admin, create_teacher, create_student
    ):
        Logger.info("Шаг 1. Создание оценки")

        grade_admin = UniversityService(university_api_utils_admin)
        teacher_id = create_teacher.id
        student_id = create_student.id
        grade = fake.random_int(1, 5)

        created_grade = grade_admin.create_grade(
            GradeRequestSchema(
                teacher_id=teacher_id, student_id=student_id, grade=grade
            )
        )

        Logger.info(f"Создана оценка: {created_grade}")
        Logger.info(f"ID созданной оценки: {created_grade.id}")

        Logger.info("Шаг 2. Проверяем что оценка действительно создана")

        grades = grade_admin.get_grades()

        assert created_grade in grades, f"Оценка {created_grade} не найдена в списке"

    def test_get_grades_stats(
            self, university_api_utils_admin, create_teacher, create_student
    ):
        """
        Проверяет, что эндпоинт статистики оценок возвращает корректные данные
        """
        grade_admin = UniversityService(university_api_utils_admin)

        Logger.info("Шаг 1. Создаем несколько оценок для теста")

        teacher_id = create_teacher.id
        student_id = create_student.id

        created_grades = TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=teacher_id,
            student_id=student_id,
        )

        Logger.info(f"Созданы оценки для статистики: {created_grades}")

        Logger.info("Шаг 2. Получаем статистику от API")
        stats = grade_admin.get_grades_stats(
            teacher_id=teacher_id,
            student_id=student_id,
        )
        Logger.info(
            f"API статистика: count={stats.count}, min={stats.min}, max={stats.max}, avg={stats.avg:.2f}"
        )

        Logger.info("Шаг 3. Получаем все оценки и считаем статистику вручную")
        all_grades = grade_admin.get_grades(
            teacher_id=teacher_id,
            student_id=student_id,
        )

        calculated = TestDataHelper.calculate_grades_stats(all_grades)

        Logger.info(
            f"Рассчитанная статистика: count={calculated['count']}, min={calculated['min']}, "
            f"max={calculated['max']}, avg={calculated['avg']:.2f}"
        )

        Logger.info("Шаг 4. Сравниваем статистику API с рассчитанной")

        expected = {
            "count": calculated["count"],
            "min": round(calculated["min"], 2),
            "max": round(calculated["max"], 2),
            "avg": round(calculated["avg"], 2)
        }

        actual = {
            "count": stats.count,
            "min": round(stats.min, 2),
            "max": round(stats.max, 2),
            "avg": round(stats.avg, 2)
        }

        assert actual == expected, (
            f"Статистика не совпадает.\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}\n"
            f"Разница: count={actual['count'] - expected['count']}, "
            f"min={actual['min'] - expected['min']}, "
            f"max={actual['max'] - expected['max']}, "
            f"avg={actual['avg'] - expected['avg']:.2f}"
        )

        Logger.info(
            f"Статистика верна: count={stats.count}, min={stats.min}, "
            f"max={stats.max}, avg={stats.avg:.2f}"
        )

    def test_update_grade(
            self, university_api_utils_admin, create_teacher, create_student
    ):
        Logger.info("Шаг 1. Создание оценки для обновления")

        grade_admin = UniversityService(university_api_utils_admin)
        teacher_id = create_teacher.id
        student_id = create_student.id
        grade = fake.random_int(1, 5)

        created_grade = grade_admin.create_grade(
            GradeRequestSchema(
                teacher_id=teacher_id, student_id=student_id, grade=grade
            )
        )

        Logger.info(f"Создана оценка для обновления: {created_grade}")
        Logger.info(f"ID созданной оценки: {created_grade.id}")

        Logger.info("Шаг 2. Обновление оценки")

        updated_grade_value = grade + 1 if grade < 5 else grade - 1
        updated_grade = grade_admin.update_grade(
            grade_id=created_grade.id,
            grade_request=GradeRequestSchema(
                teacher_id=teacher_id,
                student_id=student_id,
                grade=updated_grade_value,
            ),
        )

        Logger.info(f"Обновленная оценка: {updated_grade}")

        Logger.info("Шаг 3. Проверяем что оценка действительно обновлена")

        grades = grade_admin.get_grades()

        assert updated_grade in grades, f"Оценка {updated_grade} не найдена в списке"
        assert (
                updated_grade.id == created_grade.id
        ), f"ID оценки изменился: {updated_grade.id} != {created_grade.id}"
        assert (
                updated_grade.grade == updated_grade_value
        ), f"Оценка не обновилась: {updated_grade.grade} != {updated_grade_value}"

    def test_delete_grade(
            self, university_api_utils_admin, create_teacher, create_student
    ):
        Logger.info("Шаг 1. Создание оценки для удаления")

        grade_admin = UniversityService(university_api_utils_admin)
        teacher_id = create_teacher.id
        student_id = create_student.id
        grade = fake.random_int(1, 5)

        created_grade = grade_admin.create_grade(
            GradeRequestSchema(
                teacher_id=teacher_id, student_id=student_id, grade=grade
            )
        )

        Logger.info(f"Создана оценка для удаления: {created_grade}")
        Logger.info(f"ID созданной оценки: {created_grade.id}")

        Logger.info("Шаг 2. Удаление оценки")

        deleted_grade = grade_admin.delete_grade(grade_id=created_grade.id)

        Logger.info(f"Ответ API при удалении оценки: {deleted_grade}")

        Logger.info("Шаг 3. Проверяем что оценка действительно удалена")

        grades = grade_admin.get_grades()

        assert (
                deleted_grade.detail == "Grade deleted"
        ), f"Неожиданный ответ при удалении оценки: {deleted_grade.detail}"
        assert (
                created_grade not in grades
        ), f"Оценка {created_grade} найдена в списке после удаления"
