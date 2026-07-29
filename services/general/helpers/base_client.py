from utils.api_utils import ApiUtils

class BaseClient:
    def __init__(self, api_utils: ApiUtils):
        self.api_utils = api_utils
