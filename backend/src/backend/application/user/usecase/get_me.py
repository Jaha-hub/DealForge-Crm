from dataclasses import dataclass

from src.backend.application.auth.interfaces.security.token import TokenService
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.user.dtos.get_me import GetMeCommand, GetMeResult
from src.backend.application.user.errors import UserNotFoundError
from src.backend.domain.user.entity import User


@dataclass
class GetMeUseCase:
    """
    Сценарий получения текущего пользователя по токену

    Атрибуты:
        uow: Объект для доступа к данным
        tokens: Сервис для работы с токенами
    """
    uow: UnitOfWork
    tokens: TokenService

    async def execute(self, cmd: GetMeCommand) -> User:
        """
       Возвращает текущего пользователя на основе токена

       Args:
           cmd (GetMeCommand): Команда с токеном

       Returns:
           User: Найденный пользователь

       Raises:
           UserNotFoundError: Если пользователь не найден
       """
        async with self.uow:
            user_id = self.tokens.decode(cmd.token)
            user = await self.uow.users.get_by_id(user_id)
            if user is None:
                raise UserNotFoundError()

            return user