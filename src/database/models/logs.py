"""
model da tabelas logs
"""

from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base 
import uuid 
from sqlalchemy import UUID, DateTime, String, Integer
from datetime import datetime

class ModelLogs(Base):

    __tablename__="logs"
    id: Mapped[int]=mapped_column(Integer, primary_key=True, index=True)
    public_id: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, index=True, default=uuid.uuid4)
    log: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    

