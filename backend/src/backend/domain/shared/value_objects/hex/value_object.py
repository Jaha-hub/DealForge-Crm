import re
from dataclasses import dataclass

@dataclass(frozen=True)
class HexCode:
    value: str

    def __post_init__(self):
        pass

    def __validate(self)->bool:
        return bool(re.match(r"^#[0-9A-Fa-f]{6}$", self.value))

    def __str__(self):
        return self.value