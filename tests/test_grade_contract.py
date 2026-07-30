from services.university.helpers.grade_helper import GradeHelper


class TestGradeContract:

    def test_get_grades_status_code_ok(self, university_api_utils_admin):
        grade_helper = GradeHelper(university_api_utils_admin)

        response = grade_helper.get_grades()

        assert response.status_code == 200, (
            f"Expected status code 200, got {response.status_code}. "
            f"Response body: {response.text}"
        )

    def test_get_grades_status_code_bad_request(self, university_api_utils_admin):
        grade_helper = GradeHelper(university_api_utils_admin)

        response = grade_helper.get_grades(student_id="invalid")

        assert response.status_code == 422, (
            f"Expected status code 422, got {response.status_code}. "
            f"Response body: {response.text}"
        )

    def test_get_grades_status_code_unauthorized(self, university_api_utils_anonym):
        university_api_utils_anonym.session.headers.update(
            {"Authorization": "Bearer invalid-token"}
        )
        grade_helper = GradeHelper(university_api_utils_anonym)

        response = grade_helper.get_grades()

        assert response.status_code == 401, (
            f"Expected status code 401, got {response.status_code}. "
            f"Response body: {response.text}"
        )

    def test_get_grades_status_code_forbidden(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)

        response = grade_helper.get_grades()

        assert response.status_code == 403, (
            f"Expected status code 403, got {response.status_code}. "
            f"Response body: {response.text}"
        )

    def test_get_grades_stats_status_code_ok(self, university_api_utils_admin):
        grade_helper = GradeHelper(university_api_utils_admin)

        response = grade_helper.get_grades_stats()

        assert response.status_code == 200, (
            f"Expected status code 200, got {response.status_code}. "
            f"Response body: {response.text}"
        )

    def test_get_grades_stats_status_code_bad_request(self, university_api_utils_admin):
        grade_helper = GradeHelper(university_api_utils_admin)

        response = grade_helper.get_grades_stats(student_id="invalid")

        assert response.status_code == 422, (
            f"Expected status code 422, got {response.status_code}. "
            f"Response body: {response.text}"
        )

    def test_get_grades_stats_status_code_unauthorized(
            self, university_api_utils_anonym
    ):
        university_api_utils_anonym.session.headers.update(
            {"Authorization": "Bearer invalid-token"}
        )
        grade_helper = GradeHelper(university_api_utils_anonym)

        response = grade_helper.get_grades_stats()

        assert response.status_code == 401, (
            f"Expected status code 401, got {response.status_code}. "
            f"Response body: {response.text}"
        )

    def test_get_grades_stats_status_code_forbidden(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)

        response = grade_helper.get_grades_stats()

        assert response.status_code == 403, (
            f"Expected status code 403, got {response.status_code}. "
            f"Response body: {response.text}"
        )
