from services.auth.helpers.authorization_helper import AuthorizationHelper
from services.auth.helpers.user_helper import UserHelper
from services.auth.models.login_schema import LoginRequestsSchema, LoginResponseSchema

from services.auth.models.register_schema import RegisterRequestSchema, SuccessResponseSchema
from services.general.base_service import BaseService
from utils.api_utils import ApiUtils
from utils.config import AUTH_URL


class AuthService(BaseService):
    SERVICE_URL = AUTH_URL

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.authorization_helper = AuthorizationHelper(self.api_utils)
        self.user_helper = UserHelper(self.api_utils)

    def register_user(self, register_request: RegisterRequestSchema) -> SuccessResponseSchema:
        response = self.authorization_helper.post_register(data=register_request.model_dump())
        return SuccessResponseSchema(**response.json())

    def login_user(self, login_request: LoginRequestsSchema) -> LoginResponseSchema:
        response = self.user_helper.post_login(data=login_request.model_dump())
        return LoginResponseSchema(**response.json())
