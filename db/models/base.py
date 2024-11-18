import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone("UTC", func.current_timestamp()),
    )
    date_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.timezone("UTC", func.current_timestamp()),
        server_default=func.timezone("UTC", func.current_timestamp()),
    )
    date_deleted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
