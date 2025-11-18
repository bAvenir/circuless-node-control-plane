from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def check_postgres(db: AsyncEngine) -> dict:
    """Check PostgreSQL connection and response time"""
    try:
        start = datetime.now()
        await db.execute(text("SELECT 1"))
        duration = (datetime.now() - start).total_seconds()
        
        return {
            "status": "healthy",
            "response_time_seconds": round(duration, 3)
        }
    except Exception as e:
        logger.error(f"Postgres health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }