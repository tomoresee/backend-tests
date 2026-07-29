from pydantic import BaseModel


class RegisterRequestSchema(BaseModel):
    username: str
    password: str
    password_repeat: str
    email: str


class SuccessResponseSchema(BaseModel):
    detail: str
