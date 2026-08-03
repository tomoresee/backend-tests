from faker import Faker

from logger.logger import Logger
from services.university.constants import GradeConstants
from services.university.helpers.test_data_helpers import TestDataHelper
from services.university.models.grade_schema import GradeRequestSchema, GradeStatisticResponseSchema
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
        grade = fake.random_int(GradeConstants.MIN_GRADE, GradeConstants.MAX_GRADE)

        created_grade = grade_admin.create_grade(
            GradeRequestSchema(
                teacher_id=teacher_id, student_id=student_id, grade=grade
            )
        )

        Logger.info("Шаг 2. Проверяем что оценка действительно создана")

        grades = grade_admin.get_grades()

        assert created_grade in grades, f"Оценка {created_grade} не найдена в списке"

    def test_updated_grade_exists_in_list(
            self, university_api_utils_admin, create_grade
    ):
        Logger.info("Шаг 1. Создание оценки для обновления")

        grade_admin = UniversityService(university_api_utils_admin)

        grade = create_grade["grade"]
        grade_id = create_grade["grade_id"]
        teacher_id = create_grade["teacher_id"]
        student_id = create_grade["student_id"]

        Logger.info("Шаг 2. Обновление оценки")

        updated_grade_value = grade + 1 if grade < 5 else grade - 1
        updated_grade = grade_admin.update_grade(
            grade_id=grade_id,
            grade_request=GradeRequestSchema(
                teacher_id=teacher_id,
                student_id=student_id,
                grade=updated_grade_value,
            ),
        )

        Logger.info("Шаг 3. Проверяем что оценка есть в списке")

        grades = grade_admin.get_grades()

        assert updated_grade in grades, f"Оценка {updated_grade} не найдена в списке"

    def test_grade_update_preserves_id_and_updates_value(self, university_api_utils_admin, create_grade):
        """Проверяет, что при обновлении ID не меняется, а значение обновляется корректно"""

        Logger.info("Шаг 1. Создание оценки для обновления")

        grade_admin = UniversityService(university_api_utils_admin)

        grade = create_grade["grade"]
        grade_id = create_grade["grade_id"]
        teacher_id = create_grade["teacher_id"]
        student_id = create_grade["student_id"]

        Logger.info("Шаг 2. Обновление оценки")

        updated_grade_value = grade + 1 if grade < 5 else grade - 1
        updated_grade = grade_admin.update_grade(
            grade_id=grade_id,
            grade_request=GradeRequestSchema(
                teacher_id=teacher_id,
                student_id=student_id,
                grade=updated_grade_value,
            ),
        )

        Logger.info("Шаг 3. Проверяем, что при обновлении ID не меняется, а значение обновляется корректно")

        errors = []

        try:
            assert updated_grade.id == grade_id
        except AssertionError:
            errors.append(f"ID изменился: {updated_grade.id} != {grade_id}")

        try:
            assert updated_grade.grade == updated_grade_value
        except AssertionError:
            errors.append(f"Оценка не обновилась: {updated_grade.grade} != {updated_grade_value}")

        if errors:
            raise AssertionError("\n".join(errors))

    def test_delete_grade(self, university_api_utils_admin, create_grade):
        Logger.info("Шаг 1. Создание оценки для удаления")

        grade_admin = UniversityService(university_api_utils_admin)

        grade = create_grade["grade"]
        grade_id = create_grade["grade_id"]

        Logger.info("Шаг 2. Удаление оценки")

        grade_admin.delete_grade(grade_id=grade_id)

        Logger.info("Шаг 3. Проверяем что оценка действительно удалена")

        grades = grade_admin.get_grades()

        assert (
                grade not in grades
        ), f"Оценка {grade} найдена в списке после удаления"

    # ==========================================================
    # ========== ТЕСТЫ НА ПОЛУЧЕНИЕ СТАТИСТИКИ ОЦЕНОК ==========
    # ==========================================================

    def test_get_grades_stats(self, university_api_utils_admin, create_teacher, create_student):
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

        Logger.info("Шаг 2. Получаем статистику от API")
        stats = grade_admin.get_grades_stats(
            teacher_id=teacher_id,
            student_id=student_id,
        )

        Logger.info("Шаг 3. Получаем все оценки и считаем статистику вручную")
        all_grades = grade_admin.get_grades(
            teacher_id=teacher_id,
            student_id=student_id,
        )

        calculated = TestDataHelper.calculate_grades_stats(all_grades)

        Logger.info("Шаг 4. Сравниваем статистику API с рассчитанной")

        expected = GradeStatisticResponseSchema(
            count=calculated.count,
            min=round(calculated.min) if calculated.min is not None else None,
            max=round(calculated.max) if calculated.max is not None else None,
            avg=round(calculated.avg, 2) if calculated.avg is not None else None
        )

        actual = GradeStatisticResponseSchema(
            count=stats.count,
            min=stats.min,
            max=stats.max,
            avg=round(stats.avg, 2) if stats.avg is not None else None
        )

        assert actual == expected, (
            f"Статистика не совпадает.\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}"
        )

    def test_get_grades_stats_without_params(self, university_api_utils_admin):
        """
        Проверяет, что эндпоинт статистики работает без параметров
        Ожидаем: возвращает статистику по всем оценкам
        """
        grade_admin = UniversityService(university_api_utils_admin)
        all_grades = grade_admin.get_grades()
        stats = grade_admin.get_grades_stats()
        calculated = TestDataHelper.calculate_grades_stats(all_grades)

        expected = GradeStatisticResponseSchema(
            count=calculated.count,
            min=calculated.min,
            max=calculated.max,
            avg=round(calculated.avg, 2) if calculated.avg is not None else None
        )

        actual = GradeStatisticResponseSchema(
            count=stats.count,
            min=stats.min,
            max=stats.max,
            avg=round(stats.avg, 2) if stats.avg is not None else None
        )

        assert actual == expected, (
            f"Статистика не совпадает:\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}\n"
        )

    def test_get_grades_stats_with_teacher_id_only(self, university_api_utils_admin, create_teacher, create_student):
        """
        Проверяет фильтрацию статистики только по teacher_id
        Ожидаем: статистика только для оценок этого учителя
        """
        grade_admin = UniversityService(university_api_utils_admin)
        teacher_id = create_teacher.id
        student_id = create_student.id

        created_grades = TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=teacher_id,
            student_id=student_id,
            count=5
        )

        stats = grade_admin.get_grades_stats(teacher_id=teacher_id)

        all_grades = grade_admin.get_grades(teacher_id=teacher_id)
        expected = TestDataHelper.calculate_grades_stats(all_grades)

        actual_teacher_ids = [g.teacher_id for g in all_grades]
        assert all(t == teacher_id for t in actual_teacher_ids), (
            f"Найдены оценки других учителей.\n"
            f"Expected teacher_id: {teacher_id}\n"
            f"Actual teacher_ids: {set(actual_teacher_ids)}"
        )

        assert stats.count == expected.count, (
            f"Count не совпадает.\n"
            f"Expected: {expected.count}\n"
            f"Actual: {stats.count}"
        )

        assert stats.min == expected.min, (
            f"Min не совпадает.\n"
            f"Expected: {expected.min}\n"
            f"Actual: {stats.min}"
        )

        assert stats.max == expected.max, (
            f"Max не совпадает.\n"
            f"Expected: {expected.max}\n"
            f"Actual: {stats.max}"
        )

        actual_avg = round(stats.avg, 2)
        expected_avg = round(expected.avg, 2)
        assert actual_avg == expected_avg, (
            f"Average не совпадает.\n"
            f"Expected: {expected_avg}\n"
            f"Actual: {actual_avg}\n"
            f"Raw values - Expected: {expected.avg}, Actual: {stats.avg}"
        )

    def test_get_grades_stats_with_student_id_only(self, university_api_utils_admin, create_teacher, create_student):
        """
        Проверяет фильтрацию статистики только по student_id
        Ожидаем: статистика только для оценок этого студента
        """
        grade_admin = UniversityService(university_api_utils_admin)
        teacher_id = create_teacher.id
        student_id = create_student.id

        created_grades = TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=teacher_id,
            student_id=student_id,
            count=5
        )

        stats = grade_admin.get_grades_stats(student_id=student_id)

        all_grades = grade_admin.get_grades(student_id=student_id)
        expected = TestDataHelper.calculate_grades_stats(all_grades)

        actual_student_ids = [g.student_id for g in all_grades]
        assert all(s == student_id for s in actual_student_ids), (
            f"Найдены оценки других студентов.\n"
            f"Expected student_id: {student_id}\n"
            f"Actual student_ids: {set(actual_student_ids)}"
        )

        assert stats.count == expected.count, (
            f"Count не совпадает.\n"
            f"Expected: {expected.count}\n"
            f"Actual: {stats.count}"
        )

        assert stats.min == expected.min, (
            f"Min не совпадает.\n"
            f"Expected: {expected.min}\n"
            f"Actual: {stats.min}"
        )

        assert stats.max == expected.max, (
            f"Max не совпадает.\n"
            f"Expected: {expected.max}\n"
            f"Actual: {stats.max}"
        )

        actual_avg = round(stats.avg, 2)
        expected_avg = round(expected.avg, 2)
        assert actual_avg == expected_avg, (
            f"Average не совпадает.\n"
            f"Expected: {expected_avg}\n"
            f"Actual: {actual_avg}\n"
            f"Raw values - Expected: {expected.avg}, Actual: {stats.avg}"
        )

    def test_get_grades_stats_with_group_id_only(self, university_api_utils_admin, create_teacher, create_student,
                                                 create_group):
        """
        Проверяет фильтрацию статистики только по group_id
        Ожидаем: статистика только для оценок студентов из этой группы
        """
        grade_admin = UniversityService(university_api_utils_admin)
        teacher_id = create_teacher.id
        student_id = create_student.id
        group_id = create_group.id

        created_grades = TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=teacher_id,
            student_id=student_id,
            count=5
        )

        stats = grade_admin.get_grades_stats(group_id=group_id)
        all_grades = grade_admin.get_grades(group_id=group_id)
        expected = TestDataHelper.calculate_grades_stats(all_grades)

        actual_student_ids = [g.student_id for g in all_grades]
        assert all(s == student_id for s in actual_student_ids), (
            f"Найдены оценки студентов не из этой группы.\n"
            f"Expected student_id: {student_id}\n"
            f"Actual student_ids: {set(actual_student_ids)}"
        )

        assert stats.count == expected.count, (
            f"Count не совпадает.\n"
            f"Expected: {expected.count}\n"
            f"Actual: {stats.count}"
        )

        assert stats.min == expected.min, (
            f"Min не совпадает.\n"
            f"Expected: {expected.min}\n"
            f"Actual: {stats.min}"
        )

        assert stats.max == expected.max, (
            f"Max не совпадает.\n"
            f"Expected: {expected.max}\n"
            f"Actual: {stats.max}"
        )

        actual_avg = round(stats.avg, 2)
        expected_avg = round(expected.avg, 2)
        assert actual_avg == expected_avg, (
            f"Average не совпадает.\n"
            f"Expected: {expected_avg}\n"
            f"Actual: {actual_avg}\n"
            f"Raw values - Expected: {expected.avg}, Actual: {stats.avg}"
        )

    def test_get_grades_stats_with_teacher_id_and_student_id_params(self, university_api_utils_admin, create_teacher,
                                                                    create_student):
        """
        Проверяет фильтрацию статистики по teacher_id и student_id одновременно
        Ожидаем: статистика только для оценок этого учителя у этого студента
        """
        grade_admin = UniversityService(university_api_utils_admin)
        teacher_id = create_teacher.id
        student_id = create_student.id

        created_grades = TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=teacher_id,
            student_id=student_id,
            count=5
        )

        stats = grade_admin.get_grades_stats(
            teacher_id=teacher_id,
            student_id=student_id
        )

        all_grades = grade_admin.get_grades(
            teacher_id=teacher_id,
            student_id=student_id
        )
        expected = TestDataHelper.calculate_grades_stats(all_grades)

        actual_teacher_ids = [g.teacher_id for g in all_grades]
        assert all(t == teacher_id for t in actual_teacher_ids), (
            f"Найдены оценки других учителей.\n"
            f"Expected teacher_id: {teacher_id}\n"
            f"Actual teacher_ids: {set(actual_teacher_ids)}"
        )

        actual_student_ids = [g.student_id for g in all_grades]
        assert all(s == student_id for s in actual_student_ids), (
            f"Найдены оценки других студентов.\n"
            f"Expected student_id: {student_id}\n"
            f"Actual student_ids: {set(actual_student_ids)}"
        )

        assert stats.count == expected.count, (
            f"Count не совпадает.\n"
            f"Expected: {expected.count}\n"
            f"Actual: {stats.count}"
        )

        assert stats.min == expected.min, (
            f"Min не совпадает.\n"
            f"Expected: {expected.min}\n"
            f"Actual: {stats.min}"
        )

        assert stats.max == expected.max, (
            f"Max не совпадает.\n"
            f"Expected: {expected.max}\n"
            f"Actual: {stats.max}"
        )

        actual_avg = round(stats.avg, 2)
        expected_avg = round(expected.avg, 2)
        assert actual_avg == expected_avg, (
            f"Average не совпадает.\n"
            f"Expected: {expected_avg}\n"
            f"Actual: {actual_avg}\n"
            f"Raw values - Expected: {expected.avg}, Actual: {stats.avg}"
        )
