from fastapi import APIRouter, Query

from src.backend.application.shared.dtos.pagination import PageResult, PageRequest
from src.backend.application.source.dtos.create_source import CreateSourceCommand
from src.backend.application.source.dtos.list_source import ListSourceCommand, ListSourceSort
from src.backend.application.source.dtos.update_source import UpdateSourceCommand
from src.backend.domain.source.enums.source_tupe.enum import SourceType
from src.backend.presentation.api.v1.source.dependencies import CreateSourceDep, GetSourceDep, UpdateSourceDep, \
    ActivateSourceDep, DeactivateSourceDep, DeleteSourceDep, RegenerateWebhookSecretDep, ListSourceDep

router = APIRouter(
    prefix="/source",
    tags=["source"],
)

@router.get(
    "/"
)
async def get_sources(
        uc: ListSourceDep,
        source_type: SourceType | None = Query(None),
        is_active: bool | None = Query(None),
        q: str | None = Query(None),
        sort_by: str | None = Query(None),
        page: int = Query(default=1),
        size: int = Query(default=100),
):
    cmd = ListSourceCommand(
        type=source_type,
        is_active=is_active,
        q=q,
        sort=ListSourceSort(sort_by),
        pagination=PageRequest(
            page=page,
            size=size,
        )
    )
    result = await cmd.execute(cmd)
    return result

@router.get(
    "/{source_id}",
)
async def get_source(
        source_id: int,
        uc: GetSourceDep
):
    result = await uc.execute(
        cmd=CreateSourceCommand(source_id=source_id)
    )
    return result

@router.post(
    "/"
)
async def create_source(
        cmd: CreateSourceCommand,
        uc: CreateSourceDep
):
    result = await uc.execute(cmd)
    return result


@router.put(
    "/{source_id}",
)
async def update_source(
        cmd: UpdateSourceCommand,
        uc: UpdateSourceDep
):
    await uc.execute(cmd)

@router.post(
    "/{source_id}/activate",
)
async def activate_source(
    use_case: ActivateSourceDep,
):
    await use_case.execute()
    return {"status": "ok"}

@router.post(
    "/{source_id}/deactivate",
)
async def deactivate_source(
    use_case: DeactivateSourceDep,
):
    await use_case.execute()
    return {"status": "ok"}

@router.delete(
    "/{source_id}",
)
async def delete_source(
    use_case: DeleteSourceDep,
):
    await use_case.execute()
    return {"status": "ok"}

@router.post(
    "/{source_id}/regenerate",
)
async def regenerate_webhook_secret(
    use_case: RegenerateWebhookSecretDep,
):
    result = await use_case.execute()
    return result

