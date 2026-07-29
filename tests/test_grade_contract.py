from services.university.helpers.grade_helper import GradeHelper


class TestGradeContract:
    @staticmethod
    def _assert_validation_error_response(response):
        response_body = response.json()

        assert "detail" in response_body
        assert isinstance(response_body["detail"], list)

    def test_get_grades_status_code_ok(self, university_api_utils_admin):
        grade_helper = GradeHelper(university_api_utils_admin)

        response = grade_helper.get_grades()

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_grades_status_code_bad_request(self, university_api_utils_admin):
        grade_helper = GradeHelper(university_api_utils_admin)

        response = grade_helper.get_grades(student_id="invalid")

        assert response.status_code == 422
        self._assert_validation_error_response(response)

    def test_get_grades_status_code_unauthorized(self, university_api_utils_anonym):
        university_api_utils_anonym.session.headers.update(
            {"Authorization": "Bearer invalid-token"}
        )
        grade_helper = GradeHelper(university_api_utils_anonym)

        response = grade_helper.get_grades()

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid JWT token"

    def test_get_grades_status_code_forbidden(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)

        response = grade_helper.get_grades()

        assert response.status_code == 403
        assert response.json()["detail"] == "Access denied"

    def test_get_grades_stats_status_code_ok(self, university_api_utils_admin):
        grade_helper = GradeHelper(university_api_utils_admin)

        response = grade_helper.get_grades_stats()

        assert response.status_code == 200
        assert set(response.json()) == {"count", "min", "max", "avg"}

    def test_get_grades_stats_status_code_bad_request(self, university_api_utils_admin):
        grade_helper = GradeHelper(university_api_utils_admin)

        response = grade_helper.get_grades_stats(student_id="invalid")

        assert response.status_code == 422
        self._assert_validation_error_response(response)

    def test_get_grades_stats_status_code_unauthorized(
        self, university_api_utils_anonym
    ):
        university_api_utils_anonym.session.headers.update(
            {"Authorization": "Bearer invalid-token"}
        )
        grade_helper = GradeHelper(university_api_utils_anonym)

        response = grade_helper.get_grades_stats()

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid JWT token"

    def test_get_grades_stats_status_code_forbidden(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)

        response = grade_helper.get_grades_stats()

        assert response.status_code == 403
        assert response.json()["detail"] == "Access denied"
