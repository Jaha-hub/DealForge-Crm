from sqlalchemy import Column, String, Boolean, Integer, UUID, ForeignKey

from src.backend.infrastructure.db.sqlalchemy.core.mixins import UUIDMixin, TimestampMixin
from src.backend.infrastructure.db.sqlalchemy.core.models import Base


class FunnelModel(Base,UUIDMixin,TimestampMixin):
    __tablename__ = 'funnels'

    name = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

class FunnelStageModel(Base,UUIDMixin,TimestampMixin):
    __tablename__ = 'funnel_stages'
    funnel_id = Column(UUID(as_uuid=True), ForeignKey('funnels.id',ondelete="CASCADE"), nullable=False)
    name= Column(String(255), nullable=False)
    win_probability = Column(Integer, nullable=False)
    hex = Column(String(7), nullable=False)
    order = Column(Integer, nullable=False)