from dataclasses import dataclass
from src.backend.application.auth.dtos.change_password import ChangePasswordCommand
from src.backend.application.auth.errors import (
    InvalidPasswordError,
    SamePasswordError,
    WeakPasswordError)
from src.backend.application.auth.interfaces.security.hasher import Hasher
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User
from tests.unit.domain.shared.specification import Specification


@dataclass
class ChangePasswordUseCase:
    uow: UnitOfWork
    hasher: Hasher
    password_spec: Specification[str]
    password_diff_spec: Specification[tuple[str, str]]
    user: User

    async def execute(self, cmd: ChangePasswordCommand):
        # Проверка самого пароля
        if not self.password_spec.is_satisfied_by(cmd.new_password):
            raise WeakPasswordError("Your new password is weak")

        if not self.password_diff_spec.is_satisfied_by((cmd.old_password, cmd.new_password)):
            raise SamePasswordError("Your new password is same with old password")

        async with self.uow:

            if not self.hasher.verify(cmd.old_password, self.user.password_hash):
                raise InvalidPasswordError("Invalid password")

            self.user.change_password(self.hasher.hash(cmd.new_password))

            await self.uow.users.update(self.user)
            await self.uow.commit()