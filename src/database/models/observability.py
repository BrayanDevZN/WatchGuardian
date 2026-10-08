"""
model da tabela observability
"""
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base 
import uuid 
from sqlalchemy import UUID, DateTime, String, Integer
from datetime import datetime
from typing import Literal
class ModelObservability(Base):

    __tablename__="observability"
    id: Mapped[int]=mapped_column(Integer, primary_key=True, index=True)
    public_id: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, index=True, default=uuid.uuid4)
    status: Mapped[Literal["sucess", "pending", "failure"]] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)