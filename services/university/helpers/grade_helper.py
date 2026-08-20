from services.general.helpers.base_client import BaseClient


class GradeHelper(BaseClient):
    GRADE_ENDPOINT = "/grades/"
    GRADES_STATS_ENDPOINT = "/grades/stats/"

    def get_grades(self, student_id=None, teacher_id=None, group_id=None):
        params = {}
        if student_id is not None:
            params["student_id"] = student_id
        if teacher_id is not None:
            params["teacher_id"] = teacher_id
        if group_id is not None:
            params["group_id"] = group_id

        response = self.api_utils.get(self.GRADE_ENDPOINT, params=params)
        return response

    def post_grade(self, data: dict = None):
        response = self.api_utils.post(self.GRADE_ENDPOINT, data=data)
        return response

    def delete_grade(self, grade_id: int):
        response = self.api_utils.delete(f"{self.GRADE_ENDPOINT}{grade_id}/")
        return response

    def put_grade(self, grade_id: int, data: dict):
        response = self.api_utils.put(f"{self.GRADE_ENDPOINT}{grade_id}/", data=data)
        return response

    def get_grades_stats(self, student_id=None, teacher_id=None, group_id=None):
        params = {}
        if student_id is not None:
            params["student_id"] = student_id
        if teacher_id is not None:
            params["teacher_id"] = teacher_id
        if group_id is not None:
            params["group_id"] = group_id

        response = self.api_utils.get(self.GRADES_STATS_ENDPOINT, params=params)
        return response
