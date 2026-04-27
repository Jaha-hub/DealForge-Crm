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
    """
    Сценарий (use case) для создания нового пользователя

    Атрибуты:
        uow: Объект для управления транзакциями и доступом к БД
        hasher: Сервис для хэширования паролей
        actor: Пользователь, выполняющий действие
        password_spec: Спецификация для проверки пароля
    """
    uow: UnitOfWork
    hasher: Hasher
    actor: User
    password_spec: Specification[str]
    async def execute(
        self,
        cmd: CreateUserCommand
    ):
        """
        Создаёт нового пользователя в системе

        Args:
            cmd (CreateUserCommand): Команда с данными для создания пользователя

        Returns:
            CreateUserResult: Результат с идентификатором созданного пользователя

        Raises:
            EmailAlreadyExistsError: Если пользователь с таким email уже существует
            WeakPasswordError: Если username уже занят
            PermissionError: Если текущий пользователь не имеет прав на создание
        """
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