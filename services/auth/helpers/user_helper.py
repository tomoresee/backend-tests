import requests

from services.general.helpers.base_client import BaseClient


class UserHelper(BaseClient):
    ENDPOINT_PREFIX = "/auth"

    LOGIN_ENDPOINT = f"{ENDPOINT_PREFIX}/login/"

    def post_login(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.LOGIN_ENDPOINT, data=data)
        return response
