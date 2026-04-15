from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.user.dtos.get_me import GetMeCommand, GetMeResult
from src.backend.application.user.errors import UserNotFoundError
from src.backend.domain.user.entity import User


@dataclass
class GetMeUseCase:
    uow: UnitOfWork
    actor: User

    async def execute(self, cmd: GetMeCommand) -> GetMeResult:
        async with self.uow:
            user = await self.uow.users.get_by_id(cmd.user_id)
            if user is None:
                raise UserNotFoundError()

            return GetMeResult(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                role=user.role,
            )