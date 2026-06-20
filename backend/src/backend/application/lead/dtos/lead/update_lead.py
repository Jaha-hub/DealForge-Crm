from pydantic import BaseModel


class UpdateLeadCommand(BaseModel):
    name: str
    full_name: str
    email: str | None = None
    phone: str | None = None
    telegram: str | None = None