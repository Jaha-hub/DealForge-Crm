from dataclasses import dataclass

from pydantic import BaseModel


class LoginUserCommand(BaseModel):
    """
    Команда для авторизации
    """
    username: str
    password: str

class LoginUserResult(BaseModel):
    """
    Результат авторизации
    """
    access_token: str
    refresh_token: str
    token_type: str