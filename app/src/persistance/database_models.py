from sqlalchemy import Column, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from persistance.database import Base


class Catalog(Base):
    __tablename__ = "catalogs"

    id = Column(Text, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    catalog_data = Column(JSONB, nullable=False)


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Text, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    dataset_data = Column(JSONB, nullable=False)
