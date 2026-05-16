from dataclasses import dataclass, field
from datetime import datetime

from enum import StrEnum

from src.backend.domain.shared.entity import BaseEntity
from src.backend.domain.shared.mixins import TimeActionMixin
from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.domain.user.value_objects.username.value_object import Username

class UserRole(StrEnum):
    consultant = 'consultant'
    sales_manager = 'sales_manager'
    director = 'director'
    admin = 'admin'


@dataclass
class User(BaseEntity,TimeActionMixin):
    """
    Главная сущность пользователя

    Attributes:
    id: уникальный идентификатор
    first_name: Имя нашего пользователя
    last_name: Фамилия нашего пользователя
    username: уникальный username нашего пользователя
    email: электронная почта нашего пользователя
    password_hash: захэшированный пароль
    last_interaction: временная метка последнего взаимодействия
    is_active: флажок активности пользователя
    role: роль пользователя
    created_at: Временная метка создания сущности
    updated_at: Временная метка обновления сущности
    """
    first_name: Name
    last_name: Name
    username: Username
    email: Email
    password_hash: str
    last_interaction: datetime | None = None
    is_active: bool = field(default=True)
    role: UserRole = field(default=UserRole.consultant)
    def full_name(self)-> str:
        """
        Свойство, которое возвращает полное имя пользователя
        :return:first_name + last_name
        """
        return f'{self.first_name} {self.last_name}'

    def touch(self)->None:
        """
        Будет фиксировать время изменения
        :return:
        """
        self.updated_at = datetime.now()

    def interact(self):
        """
        Будет Фиксировать последнюю активность пользователя
        :return:
        """
        self.last_interaction = datetime.now()

    def ensure_active(self):
        """

        :return:
        """
        return self.is_active

    @classmethod
    def create(
            cls,
            first_name: str,
            last_name: str,
            username: str,
            email: str,
            password_hash: str,
            role: UserRole = UserRole.consultant,
    ):
        """
        Создаёт Объект Пользователя
        Args:
            first_name: Имя пользователя
            last_name: Фамилия Пользователя
            username: Юзернейм
            email: Электронная почта
            password_hash: хешированый пароль
        :return:
        """
        return cls(
            first_name=Name(first_name),
            last_name=Name(last_name),
            username=Username(username),
            email=Email(email),
            password_hash=password_hash,
            role=role
        )
    def __hash__(self):
        return hash(self.id)

    def change_password(
            self,
            new_password: str,
    ):
        self.password_hash = new_password
        self.touch()

    def change_first_name(
            self,
            first_name: str,
    ):
        """
        Меняет Имя пользователя
        Args:
            first_name: новое имя пользователя
        """
        self.first_name = Name(first_name)
        self.touch()

    def change_last_name(
            self,
            last_name: str,
    ):
        """
        Меняет Фамилию пользователя
        Args:
            last_name: новая фамилия пользователя
        """
        self.first_name = Name(last_name)
        self.touch()

    def change_email(self, email: str):
        """
        Меняет почту пользователя
        Args:
            email: новая почта пользователя
        """
        self.email = Email(email)
        self.touch()