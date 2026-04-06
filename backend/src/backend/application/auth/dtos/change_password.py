from dataclasses import dataclass
from uuid import UUID

from src.backend.application.auth.errors import WeakPasswordError, SamePasswordError


@dataclass(frozen=True)
class ChangePasswordCommand:
    user_id: UUID
    old_password: str
    new_password: str

    def __post_init__(self):
        if len(self.new_password) < 8:
            raise WeakPasswordError()
        if not any(c.isupper() for c in self.new_password):
            raise WeakPasswordError()

        if not any(c.isdigit() for c in self.new_password):
            raise WeakPasswordError()

        if not any(c.islower() for c in self.new_password):
            raise WeakPasswordError()

        if self.new_password == self.old_password:
            raise SamePasswordError()