from services.general.helpers.base_client import BaseClient


class TeacherHelper(BaseClient):
    TEACHERS_ENDPOINT = "/teachers/"

    def get_teachers(self):
        response = self.api_utils.get(self.TEACHERS_ENDPOINT)
        return response

    def post_teacher(self, data: dict = None, json: dict = None):
        response = self.api_utils.post(self.TEACHERS_ENDPOINT, data=data, json=json)
        return response

    def get_teacher_by_id(self, teacher_id: int):
        response = self.api_utils.get(f"{self.TEACHERS_ENDPOINT}{teacher_id}/")
        return response
