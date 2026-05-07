from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.source.dtos.get_source import GetSourceCommand, GetSourceResult
from src.backend.application.source.errors import SourceNotFoundError
from src.backend.application.source.source_view import to_result
from src.backend.domain.user.entity import User


@dataclass
class GetSourceUseCase:
    uow: UnitOfWork
    user: User
    public_user: str = "http://localhost:3000/forms"

    async def execute(
            self,
            cmd: GetSourceCommand,
    )-> GetSourceResult:
        async with self.uow:
            # policy
            source = await self.uow.source.get_by_id(cmd.source_id)
            if not source or source.is_deleted:
                raise SourceNotFoundError()
            return to_result(source)