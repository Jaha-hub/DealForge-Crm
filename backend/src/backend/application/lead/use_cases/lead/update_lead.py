from dataclasses import dataclass

from src.backend.application.lead.dtos.lead.update_lead import UpdateLeadCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import Lead
from src.backend.domain.lead.value_objects.contact.value_object import Contact
from src.backend.domain.user.entity import User


@dataclass
class UpdateLeadUseCase:
    uow: UnitOfWork
    user: User
    lead: Lead

    async def execute(self, cmd: UpdateLeadCommand) -> None:
        async with self.uow:
            self.lead.update(
                name=cmd.name,
                contact=Contact(
                    fullname=cmd.contact.fullname,
                    email=cmd.email,
                    phone=cmd.phone,
                ),
            )
            await self.uow.leads.update(self.lead)
            await self.uow.commit()
