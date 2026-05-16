from dataclasses import dataclass

from src.backend.application.auth.interfaces.security.hasher import Hasher
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.user.dtos.update_user import UpdateUserCommand, UpdateUserResult
from src.backend.application.user.errors import UserNotFoundError, UsernameAlreadyExistsError, EmailAlreadyExistsError
from src.backend.domain.user.entity import User
from src.backend.domain.user.policy.can_update_user import CanUpdateUserPolicy


@dataclass
class UpdateUserUseCase:
    """
    Сценарий обновления данных пользователя.

    Атрибуты:
        uow : Объект для управления транзакциями
        hasher : Сервис для хэширования паролей
        actor : Пользователь, выполняющий обновление
    """
    uow: UnitOfWork
    hasher: Hasher
    actor: User

    async def execute(self, cmd: UpdateUserCommand) -> UpdateUserResult:
        async with self.uow:
            CanUpdateUserPolicy(self.actor, cmd.user_id).enforce()

            user = await self.uow.users.get_by_id(cmd.user_id)
            if user is None:
                raise UserNotFoundError()

            if cmd.email is not None:
                exists_email = await self.uow.users.exists_email(cmd.email)
                if exists_email:
                    raise EmailAlreadyExistsError()
                user.email = cmd.email

            if cmd.username is not None:
                exists_username = await self.uow.users.exists_username(cmd.username)
                if exists_username:
                    raise UsernameAlreadyExistsError()
                user.username = cmd.username

            if cmd.first_name is not None:
                user.first_name = cmd.first_name

            if cmd.last_name is not None:
                user.last_name = cmd.last_name

            if cmd.password is not None:
                user.password_hash = self.hasher.hash(cmd.password)

            await self.uow.users.update(user)
            await self.uow.commit()

            return UpdateUserResult(user_id=user.id)