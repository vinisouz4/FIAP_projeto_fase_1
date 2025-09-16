from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

class TokenRefresh(BaseModel):
    access_token: str