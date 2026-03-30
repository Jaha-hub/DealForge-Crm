import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.backend.domain.shared.value_objects.email.value_object import Email


@dataclass
class User:
    id: uuid.UUID
    first_name: str
    last_name: str
    username: str # Username
    email: Email # Email
    password_hash: str # hashed_password
    last_interaction: datetime
    is_active: bool = field(default=True)
    created_at: datetime = field(default=datetime.now)
    updated_at: datetime = field(default=datetime.now)