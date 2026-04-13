import uuid
from dataclasses import dataclass

from src.backend.application.auth.errors import EmailAlreadyExistsError, WeakPasswordError
from src.backend.application.auth.interfaces.security.hasher import Hasher
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.user.dtos.create_user import CreateUserCommand, CreateUserResult
from src.backend.domain.user.entity import User
from src.backend.domain.user.policy.can_create_user import CanCreateUserPolicy
from tests.unit.domain.shared.specification import Specification


@dataclass
class CreateUserUseCase:
    uow: UnitOfWork
    hasher: Hasher
    actor: User
    password_spec: Specification[str]
    async def execute(
        self,
        cmd: CreateUserCommand
    ):
        async with self.uow:
            CanCreateUserPolicy(self.actor, cmd.role).enforce()

            exists_email = await self.uow.users.exists_email(cmd.email)
            if exists_email:
                raise EmailAlreadyExistsError()

            exists_username = await self.uow.users.exists_username(cmd.username)
            if exists_username:
                raise WeakPasswordError()

            user_id = uuid.uuid4()
            user = User.create(
                id=user_id,
                email=cmd.email,
                username=cmd.username,
                first_name=cmd.first_name,
                last_name=cmd.last_name,
                role=cmd.role,
                password_hash=self.hasher.hash(cmd.password),
            )

            await self.uow.users.create(user)

            await self.uow.commit()

            return CreateUserResult(user_id=user_id)