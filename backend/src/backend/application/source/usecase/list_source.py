from dataclasses import dataclass

from src.backend.application.shared.dtos.pagination import PageResult
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.source.dtos.get_source import GetSourceResult
from src.backend.application.source.dtos.list_source import ListSourceCommand
from src.backend.application.source.source_view import to_result
from src.backend.domain.source.entity import Source
from src.backend.domain.user.entity import User


@dataclass
class ListSourceUseCase:
    uow: UnitOfWork
    user: User


    async def execute(
            self,
            cmd: ListSourceCommand,
    ):
        async with self.uow:
            sources = await self.uow.source.list(cmd)

            return PageResult[GetSourceResult](
                items=[
                    to_result(source)
                    for source in sources.items
                ],
                page=sources.page,
                size=sources.size,
                total_items=sources.total_items,
            )