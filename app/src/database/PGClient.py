from sqlmodel import SQLModel, create_engine, Session
from utils.config import settings
import logging

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def get_session_direct():
    session = Session(engine)
    return session

def init_db():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
        