from dataclasses import dataclass

from src.backend.application.lead.dtos.lead.create_lead import CustomFieldValueOut
from src.backend.application.lead.dtos.lead.get_lead import GetLeadCommand, GetLeadResult
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import Lead
from src.backend.domain.user.entity import User


@dataclass
class GetLeadUseCase:
    uow: UnitOfWork
    user: User

    async def execute(self, cmd: GetLeadCommand):
        async with self.uow:
            lead = await self.uow.leads.get_by_id(cmd.lead_id)
            if not lead or lead.is_deleted:
                raise

            custom_field_ids = list({v.custom_field_id for v in lead.custom_values})
            fields_map = {}
            if custom_field_ids:
                fields = await self.uow.custom_fields.list_by_ids(custom_field_ids)
                fields_map = {f.id: f for f in fields}

            custom_values_out = [
                CustomFieldValueOut(
                    field_id=v.custom_field_id,
                    field_name=str(fields_map[v.custom_field_id].name)
                    if v.custom_field_id in fields_map else "",
                    field_type=str(fields_map[v.custom_field_id].field_type)
                    if v.custom_field_id in fields_map else "",
                    value_id=v.id,
                    value=str(v.value) if v.value is not None else None,
                )
                for v in lead.custom_values
            ]

        return GetLeadResult(
            id=lead.id,
            name=str(lead.name),
            fullname=str(lead.contact.fullname) if lead.contact.fullname else None,
            phone=str(lead.contact.phone) if lead.contact.phone else None,
            email=str(lead.contact.email) if lead.contact.email else None,
            telegram=lead.contact.telegram if lead.contact.telegram else None,
            funnel_id=lead.funnel_id,
            stage_id=lead.stage_id,
            source_id=lead.source_id,
            assigned_to=lead.assigned_to,
            is_deleted=lead.is_deleted,
            custom_values=custom_values_out,
            created_at=lead.created_at,
            updated_at=lead.updated_at,
        )