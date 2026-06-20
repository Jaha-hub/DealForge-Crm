from src.backend.application.lead.dtos.lead.create_lead import CreateLeadCommand, CreateLeadResult
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.source.dtos.list_source import ListSourceCommand
from src.backend.domain.funnel.entity import StageKind
from src.backend.domain.lead.entity import Lead
from src.backend.domain.lead.value_objects.contact.value_object import Contact
from src.backend.domain.source.enums.source_tupe.enum import SourceType
from src.backend.domain.user.entity import User


class CreateLeadUseCase:
    uow: UnitOfWork
    user: User

    async def execute(self, cmd: CreateLeadCommand):
        async with self.uow:
            funnel = await self.uow.funnels.get_funnel_by_id(cmd.funnel_id)
            if not funnel:
                raise
            stages = await self.uow.stages.get_funnel_stages(funnel.id)

            stage_id = None
            for stage in stages:
                if stage.kind == StageKind.initial:
                    stage_id = stage.id
                    break
            if stage_id is None:
                raise

            sources = await self.uow.source.list(ListSourceCommand(type=SourceType.manual))
            source_id = None
            for source in sources.items:
                source_id = source.id
            if source_id is None:
                raise

            assigned_to = await self.uow.users.get_by_id(cmd.assigned_to)
            if not assigned_to:
                raise

            lead = Lead.create(
                name=cmd.name,
                stage_id=stage_id,
                funnel_id=funnel.id,
                assigned_to=assigned_to,
                source_id=source_id,
                contact=Contact(
                    fullname=cmd.fullname,
                    email=cmd.email,
                    phone=cmd.phone,
                    telegram=cmd.telegram,
                )
            )
            await self.uow.leads.add(lead)
            await self.uow.commit()

            duplicates = await self.uow.leads.get_duplicates(
                phone=cmd.phone,
                email=cmd.email,
                telegram=cmd.telegram,
            )
            warning = len(duplicates) != 0
            await self.uow.leads.add(lead)
            await self.uow.commit()

        return CreateLeadResult(
            lead_id=lead.id,
            duplicate_warning=warning,
            duplicated_lead_ids=[
                lead.id for lead in duplicates
            ]
        )