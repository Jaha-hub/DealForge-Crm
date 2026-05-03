from dataclasses import dataclass

from src.backend.application.auth.dtos.login_user import LoginUserCommand, LoginUserResult
from src.backend.application.auth.errors import AuthUserNotFoundError, InvalidPasswordError, InactiveUserError, \
    InActiveUserError
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.auth.interfaces.security.hasher import Hasher
from src.backend.application.auth.interfaces.security.token import TokenService

@dataclass
class LoginUserUseCase:
    """
    Сценарий Авторизации пользователя
    Attributes:
        uow: Менеджер сессий
        tokens: Сервис токенов
        hasher: Сервис хеширования пароля
    """
    uow: UnitOfWork
    tokens: TokenService
    hasher: Hasher

    async def execute(
            self,
            cmd: LoginUserCommand,
    )->LoginUserResult:
        """
        Запуск Сценария Авторизации

        Args:
            cmd: команда для авторизации

        Returns:
            токены авторизации

        Raises:
            AuthUserNotFoundError: если пользователь ввёл неправильное имя
            InvalidPasswordError: если пользователь ввёл неправильный пароль
            InactiveUserError: если пользователь не активный
        """
        async with self.uow:
            user = await self.uow.users.get_by_username(cmd.username)

            if not user:
                raise AuthUserNotFoundError("Invalid password or username")

            if not self.hasher.verify(cmd.password, user.password_hash):
                raise InvalidPasswordError("Invalid password or username")

            if not user.ensure_active():
                raise InActiveUserError("User is not active")

            access_token = self.tokens.encode(user.id)
            refresh_token = self.tokens.encode(user.id, is_refresh=True)
            token_type = self.tokens.get_token_type()

            user.interact()

            await self.uow.users.update(user)
            await self.uow.commit()

            return LoginUserResult(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type=token_type,
            )