from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.application.user.repository import UserRepository
from src.backend.domain.user.entity import User


class SqlalchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User:
        pass

    async def get_by_username(self, username: str) -> User:
        pass

    async def get_by_email(self, email: str) -> User:
        pass

    async def create(self, user: User) -> User:
        pass

    async def update(self, user: User) -> None:
        pass

    async def delete(self, user: User) -> None:
        pass

