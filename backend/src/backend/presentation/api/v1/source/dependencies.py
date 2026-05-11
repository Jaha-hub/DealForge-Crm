from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.application.source.usecase.activate_source import ActivateSourceUseCase
from src.backend.application.source.usecase.create_source import CreateSourceUseCase
from src.backend.application.source.usecase.deactivate import DeactivateSourceUseCase
from src.backend.application.source.usecase.delete_source import DeleteSourceUseCase
from src.backend.application.source.usecase.get_source import GetSourceUseCase
from src.backend.application.source.usecase.list_source import ListSourceUseCase
from src.backend.application.source.usecase.regenerate_webhook_secret import RegenerateWebhookSecretUseCase
from src.backend.application.source.usecase.update_source import UpdateSourceUseCase
from src.backend.domain.source.entity import Source
from src.backend.infrastructure.db.sqlalchemy.source.repository import SQLAlchemySourceRepository
from src.backend.presentation.api.v1.auth.dependencies import CurrentUserDep
from src.backend.presentation.api.v1.core.dependencies import UoWDep, get_db


async def get_source_repo(
        session: AsyncSession= Depends(get_db),
)->SQLAlchemySourceRepository:
    return SQLAlchemySourceRepository(
        session=session,
    )

SourceRepoDep = Annotated[
    SQLAlchemySourceRepository,
    Depends(get_source_repo),
]



def get_create_source_use_case(
        uow: UoWDep,
        user: CurrentUserDep,
)->CreateSourceUseCase:
    return CreateSourceUseCase(
        uow=uow,
        user=user,
    )

CreateSourceDep = Annotated[
    CreateSourceUseCase,
    Depends(get_create_source_use_case)
]

def get_source_use_case(
        uow: UoWDep,
        user: CurrentUserDep,
)->GetSourceUseCase:
    return GetSourceUseCase(
        uow=uow,
        user=user,
    )

GetSourceDep = Annotated[
    GetSourceUseCase,
    Depends(get_source_use_case)
]

async def get_current_source(
        source_id: UUID,
        repo: SourceRepoDep,
)->Source:
    source =await repo.get_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

CurrentSourceDep = Annotated[
    Source,
    Depends(get_current_source)
]

def get_update_source_use_case(
    uow: UoWDep,
    user: CurrentUserDep,
    source: CurrentSourceDep
) -> UpdateSourceUseCase:
    return UpdateSourceUseCase(
        uow=uow,
        user=user,
        source=source
    )

UpdateSourceDep = Annotated[
    UpdateSourceUseCase,
    Depends(get_update_source_use_case)
]


def get_activate_source_use_case(
    uow: UoWDep,
    user: CurrentUserDep,
    source: CurrentSourceDep
) -> ActivateSourceUseCase:
    return ActivateSourceUseCase(
        uow=uow,
        user=user,
        source=source
    )

ActivateSourceDep = Annotated[
    ActivateSourceUseCase,
    Depends(get_activate_source_use_case)
]

def get_deactivate_source_use_case(
    uow: UoWDep,
    user: CurrentUserDep,
    source: CurrentSourceDep
) -> DeactivateSourceUseCase:
    return DeactivateSourceUseCase(
        uow=uow,
        user=user,
        source=source
    )

DeactivateSourceDep = Annotated[
    DeactivateSourceUseCase,
    Depends(get_deactivate_source_use_case)
]

def get_delete_source_use_case(
    uow: UoWDep,
    user: CurrentUserDep,
    source: CurrentSourceDep
) -> DeleteSourceUseCase:
    return DeleteSourceUseCase(
        uow=uow,
        user=user,
        source=source
    )

DeleteSourceDep = Annotated[
    DeleteSourceUseCase,
    Depends(get_delete_source_use_case)
]


def get_regenerate_webhook_secret_use_case(
    uow: UoWDep,
    user: CurrentUserDep,
    source: CurrentSourceDep
) -> RegenerateWebhookSecretUseCase:
    return RegenerateWebhookSecretUseCase(
        uow=uow,
        user=user,
        source=source
    )

RegenerateWebhookSecretDep = Annotated[
    RegenerateWebhookSecretUseCase,
    Depends(get_regenerate_webhook_secret_use_case)
]

def get_list_source_use_case(
        uow: UoWDep,
        user: CurrentUserDep,
)->ListSourceUseCase:
    return ListSourceUseCase(
        uow=uow,
        user=user,
    )

ListSourceDep = Annotated[
    ListSourceUseCase,
    Depends(get_list_source_use_case)
]