from uuid import UUID

from sqlalchemy import select, Select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.application.funnel.dtos.list_funnel import ListFunnelCommand, FunnelSortEnum
from src.backend.application.funnel.repository import FunnelRepository
from src.backend.application.shared.dtos.pagination import PageResult
from src.backend.domain.funnel.entity import Funnel
from src.backend.domain.shared.value_objects.name.value_object import Name
from src.backend.infrastructure.db.sqlalchemy.funnel.models import FunnelModel


def to_entity(funnel: FunnelModel) -> Funnel:
    return Funnel(
        id=funnel.id,
        name=Name(funnel.name),
        is_deleted=bool(funnel.is_deleted),
        created_at=funnel.created_at,
        updated_at=funnel.updated_at,
    )

def to_model(funnel: Funnel) -> FunnelModel:
    return FunnelModel(
        id=funnel.id,
        name=funnel.name.value,
        is_deleted=bool(funnel.is_deleted),
        created_at=funnel.created_at,
        updated_at=funnel.updated_at,
    )


class SqlAlchemyFunnelRepository(FunnelRepository):
    SORT_COLUMNS = {
        FunnelSortEnum.name_asc: FunnelModel.name.asc(),
        FunnelSortEnum.name_desc: FunnelModel.name.desc(),
        FunnelSortEnum.created_at_asc: FunnelModel.created_at.asc(),
        FunnelSortEnum.created_at_desc: FunnelModel.created_at.desc()
    }
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_funnel(self, funnel: Funnel) -> Funnel:
        instance = to_model(funnel)
        self.session.add(instance)
        await self.session.flush()
        return to_entity(instance)

    async def update_funnel(self, funnel: Funnel) -> Funnel:
        instance = to_model(funnel)
        self.session.add(instance)
        await self.session.flush()
        return to_entity(instance)

    async def delete_funnel(self, funnel: Funnel) -> None:
        instance = to_model(funnel)
        self.session.add(instance)
        await self.session.flush()

    async def get_funnel_by_id(self, funnel_id: UUID) -> Funnel | None:
        stmt = select(FunnelModel).where(FunnelModel.id == funnel_id)
        result = await self.session.execute(stmt)
        funnel = result.scalar_one_or_none()
        return to_entity(funnel) if funnel else None

    def _apply_filters(self, stmt: Select, q:str | None = None) -> Select:
        if q:
            stmt = stmt.where(FunnelModel.name.ilike(f"%{q}%"))

    def __apply_sort(self, stmt: Select, sort_by: FunnelSortEnum, q:str | None = None) -> Select:
        if not sort_by in self.SORT_COLUMNS:
            return stmt
        return stmt.order_by(self.SORT_COLUMNS[sort_by])

    async def _count(self, base_stmt: Select) -> int:
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        result = await self.session.execute(count_stmt)
        return result.scalar_one_or_none()

    async def get_funnels(self, cmd: ListFunnelCommand) -> PageResult[Funnel]:
        stmt = select(FunnelModel)
        stmt= self._apply_filters(stmt.cmd.q)
        total = await self._count(stmt)

        if total == 0:
            return PageResult.empty()

        stmt = self.__apply_sort(stmt,cmd.sort_by)
        stmt = stmt.limit(cmd.paginatio.limit).offset(cmd.paginatio.offset)

        result = await self.session.execute(stmt)
        funnels = result.scalars().all()

        return PageResult(
            items=[to_entity(funnel) for funnel in funnels],
            total_items=total,
            page=cmd.paginatio.page,
            size=cmd.paginatio.limit,
        )