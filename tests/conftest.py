import random

import pytest

from services.auth.auth_service import AuthService
from services.auth.models.login_schema import LoginRequestsSchema
from services.auth.models.register_schema import RegisterRequestSchema
from services.university.constants import GradeConstants
from services.university.models.grade_schema import GradeRequestSchema
from services.university.models.group_schema import GroupRequestSchema, Degree
from services.university.models.student_schema import StudentRequestSchema
from services.university.models.teachers_schema import TeacherRequestSchema, Subject
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils
from faker import Faker

fake = Faker()


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def access_token(auth_api_utils_anonym):
    auth_service = AuthService(auth_api_utils_anonym)
    username = fake.user_name()
    password = fake.password(
        length=30, special_chars=True, digits=True, upper_case=True, lower_case=True
    )

    auth_service.register_user(
        register_request=RegisterRequestSchema(
            username=username,
            password=password,
            password_repeat=password,
            email=fake.email(),
        )
    )

    login_response = auth_service.login_user(
        login_request=LoginRequestsSchema(username=username, password=password)
    )
    return login_response.access_token


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(
        url=AuthService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"}
    )
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(
        url=UniversityService.SERVICE_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def create_teacher(university_api_utils_admin):
    university_admin = UniversityService(university_api_utils_admin)

    first_name = fake.first_name()
    last_name = fake.last_name()
    subject = random.choice([s.value for s in Subject])

    teacher = university_admin.create_teacher(
        TeacherRequestSchema(
            first_name=first_name, last_name=last_name, subject=subject
        )
    )

    return teacher


@pytest.fixture(scope="function", autouse=False)
def create_group(university_api_utils_admin):
    university_admin = UniversityService(university_api_utils_admin)
    name = fake.name()
    group = university_admin.create_group(GroupRequestSchema(name=name))

    return group


@pytest.fixture(scope="function", autouse=False)
def create_student(university_api_utils_admin, create_group):
    university_admin = UniversityService(university_api_utils_admin)

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    degree = random.choice([d.value for d in Degree])
    phone = fake.numerify("+7##########")
    group_id = create_group.id

    student = university_admin.create_student(
        StudentRequestSchema(
            first_name=first_name,
            last_name=last_name,
            email=email,
            degree=degree,
            phone=phone,
            group_id=group_id,
        )
    )

    return student


@pytest.fixture(scope="function", autouse=False)
def create_grade(university_api_utils_admin, create_teacher, create_student, create_group):
    university_admin = UniversityService(university_api_utils_admin)

    teacher_id = create_teacher.id
    student_id = create_student.id
    grade = fake.random_int(GradeConstants.MIN_GRADE, GradeConstants.MAX_GRADE)

    created_grade = university_admin.create_grade(
        GradeRequestSchema(
            teacher_id=teacher_id, student_id=student_id, grade=grade
        )
    )

    return {
        "grade": grade,
        "grade_id": created_grade.id,
        "teacher_id": teacher_id,
        "student_id": student_id
    }
