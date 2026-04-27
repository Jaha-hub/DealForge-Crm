from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.user.dtos.delete_user import DeleteUserCommand, DeleteUserResult
from src.backend.application.user.errors import UserNotFoundError
from src.backend.domain.shared.policy import Policy
from src.backend.domain.user.entity import User, UserRole
from src.backend.domain.user.policy.can_delete_user import CanDeleteUserPolicy


@dataclass
class DeleteUserUseCase:
    """
    Сценарий удаления пользователя

    Атрибуты:
        uow: Объект для работы с транзакциями
        actor: Пользователь, выполняющий удаление
        """
    uow: UnitOfWork
    actor: User

    async def execute(
            self,
            cmd: DeleteUserCommand
    ) -> DeleteUserResult:
        """
        Удаляет пользователя по ID.

        Args:
            cmd (DeleteUserCommand): Команда с ID пользователя

        Returns:
            DeleteUserResult: Результат с ID удалённого пользователя

        Raises:
            UserNotFoundError: Если пользователь не найден
            PermissionError: Если нет прав на удаление
        """
        async with self.uow:
            target_user = await self.uow.users.get_by_id(cmd.user_id)

            if not target_user:
                raise UserNotFoundError()

            CanDeleteUserPolicy(self.actor, target_user).enforce()

            await self.uow.users.delete(target_user)
            await self.uow.commit()

            return DeleteUserResult(user_id=target_user.id)