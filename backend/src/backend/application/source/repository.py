from typing import Protocol
from uuid import UUID

from src.backend.application.shared.dtos.pagination import PageResult
from src.backend.application.source.dtos.list_source import ListSourceCommand
from src.backend.domain.source.entity import Source


class SourceRepository(Protocol):
    async def add(self, source: Source) -> Source: ...

    async def update(self, source: Source) -> Source: ...

    async def exists_slug(self, slug: str) -> bool: ...

    async def get_by_id(self,source_id:UUID)-> Source | None:...

    async def list(self, cmd: ListSourceCommand) -> PageResult[Source]: ...