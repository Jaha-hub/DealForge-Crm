from typing import Protocol

from src.backend.domain.source.entity import Source


class SourceRepository(Protocol):
    async def add(self, source: Source) -> Source: ...

    async def update(self, source: Source) -> Source: ...

    async def exists_slug(self, slug: str) -> bool: ...

