from services.general.helpers.base_client import BaseClient


class GroupHelper(BaseClient):
    GROUP_ENDPOINT = "/groups/"

    def get_groups(self):
        response = self.api_utils.get(self.GROUP_ENDPOINT)
        return response

    def post_group(self, data: dict = None, json: dict = None):
        response = self.api_utils.post(self.GROUP_ENDPOINT, data=data, json=json)
        return response

    def get_group_by_id(self, group_id: int):
        response = self.api_utils.get(f"{self.GROUP_ENDPOINT}{group_id}/")
        return response
