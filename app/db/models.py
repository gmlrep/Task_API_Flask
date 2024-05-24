from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, func, JSON, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Tasks(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    title: Mapped[str] = mapped_column(String(24))
    description: Mapped[str] = mapped_column(String(128), nullable=True)
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(server_default=func.now())
