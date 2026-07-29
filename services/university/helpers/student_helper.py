from services.general.helpers.base_client import BaseClient


class StudentHelper(BaseClient):
    STUDENT_ENDPOINT = "/students/"

    def get_students(self):
        response = self.api_utils.get(self.STUDENT_ENDPOINT)
        return response

    def post_student(self, data: dict = None, json: dict = None):
        response = self.api_utils.post(self.STUDENT_ENDPOINT, data=data, json=json)
        return response

    def get_student_by_id(self, student_id: int):
        response = self.api_utils.get(f"{self.STUDENT_ENDPOINT}{student_id}/")
        return response
