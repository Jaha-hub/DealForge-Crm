import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.domain.user.value_objects.username.value_object import Username


@dataclass
class User:
    """
    Главная сущность пользователя
    """
    id: uuid.UUID
    first_name: Name
    last_name: Name
    username: Username
    email: Email
    password_hash: str # hashed_password
    last_interaction: datetime | None = None
    is_active: bool = field(default=True)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

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
            id: uuid.UUID,
            first_name: str,
            last_name: str,
            username: str,
            email: str,
            password_hash: str,
    ):
        """
        Создаёт Объект Пользователя
        :param id: Индивидуальный Идентификатор
        :param first_name: Имя пользователя
        :param last_name: Фамилия Пользователя
        :param username: Юзернейм
        :param email: Электронная почта
        :param password_hash: хешированый пароль
        :return:
        """
        return cls(
            id=id,
            first_name=Name(first_name),
            last_name=Name(last_name),
            username=Username(username),
            email=Email(email),
            password_hash=password_hash
        )
    def __hash__(self):
        return hash(self.id)

    def change_password(
            self,
            new_password: str,
    ):
        self.password_hash = new_password
        self.touch()