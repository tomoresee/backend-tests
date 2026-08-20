import requests

from services.general.helpers.base_client import BaseClient


class AuthorizationHelper(BaseClient):
    ENDPOINT_PREFIX = "/auth"

    REGISTER_ENDPOINT = f"{ENDPOINT_PREFIX}/register/"

    def post_register(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.REGISTER_ENDPOINT, data=data)
        return response
