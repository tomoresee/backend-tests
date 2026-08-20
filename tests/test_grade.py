import allure
from faker import Faker

from logger.logger import Logger
from services.university.constants import GradeConstants
from services.university.helpers.test_data_helpers import TestDataHelper
from services.university.models.grade_schema import GradeRequestSchema, GradeStatisticResponseSchema
from services.university.models.teachers_schema import Subject, TeacherRequestSchema
from services.university.university_service import UniversityService
from utils.assertions import soft_assert

fake = Faker()


class TestGrade:

    @allure.epic("University Service")
    @allure.feature("Grade Management")
    @allure.story("Create Grade")
    @allure.title("Создание оценки и проверка её наличия в списке")
    def test_create_grade(
            self, university_api_utils_admin, create_teacher, create_student
    ):
        with allure.step("Создание оценки"):
            Logger.info("Шаг 1. Создание оценки")

            grade_admin = UniversityService(university_api_utils_admin)
            teacher_id = create_teacher.id
            student_id = create_student.id
            grade = fake.random_int(GradeConstants.MIN_GRADE, GradeConstants.MAX_GRADE)

            created_grade = grade_admin.create_grade(
                GradeRequestSchema(
                    teacher_id=teacher_id,
                    student_id=student_id,
                    grade=grade
                )
            )

            allure.attach(
                f"Teacher ID: {teacher_id}\nStudent ID: {student_id}\nGrade: {grade}",
                name="Параметры созданной оценки",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверка что оценка действительно создана"):
            Logger.info("Шаг 2. Проверяем что оценка действительно создана")

            grades = grade_admin.get_grades()

            with allure.step(f"Поиск оценки с ID {created_grade.id} в списке"):
                assert created_grade in grades, f"Оценка {created_grade} не найдена в списке"
                Logger.info(f"Оценка {created_grade} успешно найдена в списке")

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

        updated_grade_value = grade + 1 if grade < GradeConstants.MAX_GRADE else grade - 1
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

        with soft_assert() as check:
            check(updated_grade.id == grade_id, f"ID изменился: {updated_grade.id} != {grade_id}")
            check(updated_grade.grade == updated_grade_value,
                  f"Оценка не обновилась: {updated_grade.grade} != {updated_grade_value}")

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

    def test_get_grades_stats(self, university_api_utils_admin, create_teacher, create_student):
        """
        Проверяет, что эндпоинт статистики оценок возвращает корректные данные
        """
        grade_admin = UniversityService(university_api_utils_admin)

        Logger.info("Шаг 1. Создаем несколько оценок для теста")

        teacher_id = create_teacher.id
        student_id = create_student.id

        TestDataHelper.create_multiple_grades(
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

    def test_get_grades_stats_with_teacher_id_only(self, university_api_utils_admin, create_teacher,
                                                   create_student):
        grade_admin = UniversityService(university_api_utils_admin)

        # 1. Создаем ЦЕЛЕВОГО учителя и его оценки
        target_teacher_id = create_teacher.id
        student_id = create_student.id

        target_grades = TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=target_teacher_id,
            student_id=student_id,
            count=5
        )

        # 2. Создаем ВТОРОГО учителя и его оценки

        first_name = fake.first_name()
        last_name = fake.last_name()
        subject = Subject.MATHEMATICS

        second_teacher = grade_admin.create_teacher(
            TeacherRequestSchema(first_name=first_name, last_name=last_name, subject=subject))

        TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=second_teacher.id,
            student_id=student_id,
            count=3
        )

        # 3. Выполняем действие
        stats = grade_admin.get_grades_stats(teacher_id=target_teacher_id)

        # 4. Проверки
        expected_stats = TestDataHelper.calculate_grades_stats(target_grades)

        assert stats == expected_stats, (
            f"Статистика не совпадает.\n"
            f"Expected: {expected_stats}\n"
            f"Actual: {stats}"
        )

    def test_get_grades_stats_with_student_id_only(self, university_api_utils_admin, create_teacher, create_student,
                                                   student_factory, group_factory):
        grade_admin = UniversityService(university_api_utils_admin)
        teacher_id = create_teacher.id

        # 1. Целевой студент и его оценки
        target_student_id = create_student.id

        target_grades = TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=teacher_id,
            student_id=target_student_id,
            count=5
        )

        # 2. ДРУГОЙ студент с оценками от того же учителя
        group = group_factory()
        other_student = student_factory(group_id=group.id)

        TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=teacher_id,
            student_id=other_student.id,
            count=3
        )

        # 3. Выполняем действие
        stats = grade_admin.get_grades_stats(student_id=target_student_id)

        # 4. Сравнение с эталоном
        expected = TestDataHelper.calculate_grades_stats(target_grades)

        assert stats == expected, (
            f"Статистика не совпадает.\n"
            f"Expected: {expected}\n"
            f"Actual: {stats}"
        )

    def test_get_grades_stats_with_group_id_only(self, university_api_utils_admin, create_teacher, create_student,
                                                 create_group, group_factory, student_factory):
        grade_admin = UniversityService(university_api_utils_admin)
        teacher_id = create_teacher.id

        # 1. Создаем ЦЕЛЕВУЮ группу и её оценки
        target_group_id = create_group.id
        target_student_id = create_student.id

        target_grades = TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=teacher_id,
            student_id=target_student_id,
            count=5
        )

        # 2. Создаем ВТОРУЮ группу и её оценки
        group = group_factory()
        second_student = student_factory(group_id=group.id)

        TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=teacher_id,
            student_id=second_student.id,
            count=3
        )

        # 3. Выполняем действие
        stats = grade_admin.get_grades_stats(group_id=target_group_id)

        # 4. Проверки
        expected_stats = TestDataHelper.calculate_grades_stats(target_grades)

        assert stats == expected_stats, (
            f"Статистика не совпадает.\n"
            f"Expected: {expected_stats}\n"
            f"Actual: {stats}"
        )

    def test_get_grades_stats_with_teacher_id_and_student_id_params(self, university_api_utils_admin, create_teacher,
                                                                    create_student, group_factory, student_factory):
        grade_admin = UniversityService(university_api_utils_admin)

        # 1. Целевая пара: учитель + студент
        target_teacher_id = create_teacher.id
        target_student_id = create_student.id

        target_grades = TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=target_teacher_id,
            student_id=target_student_id,
            count=5
        )

        # 2. Тот же учитель, но ДРУГОЙ студент
        group = group_factory()
        other_student = student_factory(group_id=group.id)

        TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=target_teacher_id,
            student_id=other_student.id,
            count=3
        )

        # 3. ДРУГОЙ учитель, но тот же студент
        first_name = fake.first_name()
        last_name = fake.last_name()
        subject = Subject.MATHEMATICS

        other_teacher = grade_admin.create_teacher(
            TeacherRequestSchema(
                first_name=first_name,
                last_name=last_name,
                subject=subject))

        TestDataHelper.create_multiple_grades(
            grade_admin=grade_admin,
            teacher_id=other_teacher.id,
            student_id=target_student_id,
            count=3
        )

        # 4. Выполняем действие
        stats = grade_admin.get_grades_stats(
            teacher_id=target_teacher_id,
            student_id=target_student_id
        )

        # 5. Сравнение с эталоном из setup
        expected = TestDataHelper.calculate_grades_stats(target_grades)

        assert stats == expected, (
            f"Статистика не совпадает.\n"
            f"Expected: {expected}\n"
            f"Actual: {stats}"
        )
