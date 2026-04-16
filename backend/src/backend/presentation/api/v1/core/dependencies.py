from typing import AsyncGenerator

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.infrastructure.db.sqlalchemy.core.session import async_session
from src.backend.infrastructure.db.sqlalchemy.core.uow import SqlalchemyUnitOfWork


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()

async def get_uow(
        session: AsyncSession= Depends(get_db),
)->SqlalchemyUnitOfWork:
    return SqlalchemyUnitOfWork(
        session=session
    )