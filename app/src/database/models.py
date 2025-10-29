from sqlmodel import SQLModel, Field, Column
from datetime import datetime
from typing import Any
import uuid
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from utils.config import settings

class Item(SQLModel, table=True):
    __tablename__ = settings.DATABASE_TABLE

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    json_data: dict = Field(sa_column=Column(JSONB, nullable=False), description="Arbitrary JSON payload")
