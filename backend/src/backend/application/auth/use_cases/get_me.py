from dataclasses import dataclass

from src.backend.application.auth.dtos.get_me import GetMeCommand
from src.backend.application.auth.errors import InactiveUserError
from src.backend.application.auth.interfaces.security.token import TokenService
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User


@dataclass
class GetMeUseCase:
    """
    Сценарий получения себя
    Attributes:
        uow: Менеджер сессий
        tokens: Сервис токенов
    """
    uow: UnitOfWork
    tokens: TokenService

    async def execute(
            self,
            cmd: GetMeCommand,
    )->User:
        """
        Запуск сценария нахождения самого себя
        Args:
            cmd: команда для нахождения самого себя
        Returns:
            пользователь
        Raises:
            InactiveUserError: пользователь не в сети
        """
        async with self.uow:
             user_id = self.tokens.decode(cmd.token)

             user = await self.uow.users.get_by_id(user_id)

             if not user:
                 raise InactiveUserError()
             return user