import random

from faker import Faker

from logger.logger import Logger
from services.university.models.teachers_schema import Subject, TeacherRequestSchema
from services.university.university_service import UniversityService

fake = Faker()


class TestTeacher:
    def test_create_teacher(self, university_api_utils_admin):
        university_admin = UniversityService(university_api_utils_admin)

        Logger.info("Шаг 1. Создание учителя")

        first_name = fake.first_name()
        last_name = fake.last_name()
        subject = random.choice([s.value for s in Subject])

        created_teacher = university_admin.create_teacher(
            TeacherRequestSchema(
                first_name=first_name, last_name=last_name, subject=subject
            )
        )

        Logger.info(f"Создан учитель: {created_teacher}")
        Logger.info(f"ID созданного учителя: {created_teacher.id}")

        Logger.info("Шаг 2. Проверяем что учитель действительно создан")

        teachers = university_admin.get_teachers()

        assert (
                created_teacher in teachers
        ), f"Учитель {created_teacher} не найден в списке"
