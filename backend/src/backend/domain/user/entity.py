import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.backend.domain.shared.value_objects.email.value_object import Email
from src.backend.domain.shared.value_objects.name.value_object import Name


@dataclass
class User:
    id: uuid.UUID
    first_name: Name
    last_name: Name
    username: str # Username
    email: Email # Email
    password_hash: str # hashed_password
    last_interaction: datetime
    is_active: bool = field(default=True)
    created_at: datetime = field(default=datetime.now)
    updated_at: datetime = field(default=datetime.now)