import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import func
from sqlalchemy import update, delete, cast
from sqlalchemy.dialects.postgresql import JSONPATH
from typing import List, Optional
from sqlalchemy.types import UserDefinedType
from persistance.tables import ThingDescriptionDB

URN = "urn:circ:<org>:wot:<uuid>"

class ThingDescriptionCRUD:
    
    @staticmethod
    async def create(db: AsyncSession, td_data: dict) -> ThingDescriptionDB:
        """Create a new Thing Description"""

        oid=uuid.uuid4()
        td=td_data
        td['oid']=str(oid)
        db_td = ThingDescriptionDB(
            oid=oid,
            td=td
        )
        db.add(db_td)
        await db.commit()
        await db.refresh(db_td)
        return db_td
    
    @staticmethod
    async def get_by_id(db: AsyncSession, td_id: int) -> Optional[ThingDescriptionDB]:
        """Get Thing Description by ID"""
        result = await db.execute(select(ThingDescriptionDB).filter(ThingDescriptionDB.id == td_id))
        return result.scalars().first()
    
    # @staticmethod
    # async def get_by_oid(db: AsyncSession, oid: uuid.UUID) -> Optional[ThingDescriptionDB]:
    #     """Get Thing Description by OID"""
    #     result = await db.execute(select(ThingDescriptionDB).filter(ThingDescriptionDB.oid == oid))
    #     return result.scalars().first()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ThingDescriptionDB]:
        """Get all Thing Descriptions with pagination"""
        result = await db.execute(select(ThingDescriptionDB).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def update(db: AsyncSession, td_id: int, td_data: dict) -> Optional[ThingDescriptionDB]:
        """Update Thing Description"""
        await db.execute(
            update(ThingDescriptionDB)
            .where(ThingDescriptionDB.id == td_id)
            .values(td=td_data)
        )
        await db.commit()
        return await ThingDescriptionCRUD.get_by_id(db, td_id)
    
    @staticmethod
    async def delete(db: AsyncSession, td_id: int) -> bool:
        """Delete Thing Description"""
        result = await db.execute(
            delete(ThingDescriptionDB)
            .where(ThingDescriptionDB.id == td_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def jsonpath_query(
        db: AsyncSession,
        jsonpath_query: str,
        max_results: int = 10 
    ) -> List['ThingDescriptionDB']:
        """
        Simple async version that fetches all results in a single query.
        More efficient when you expect to find enough matches quickly.
        
        Args:
            session: SQLAlchemy AsyncSession
            jsonpath_query: PostgreSQL JSONPath expression
            max_results: Maximum number of results
            
        Returns:
            List of matching TD documents
        """
        
        stmt = (
            select(ThingDescriptionDB)
            .where(
                func.jsonb_path_exists(
                    ThingDescriptionDB.td,
                    cast(jsonpath_query, JSONPATH)
                )
            )
            .order_by(ThingDescriptionDB.id)
            .limit(max_results)
        )
        
        result = await db.execute(stmt)
        rows = result.scalars().all()
        
        return [
            {
                "id": row.id,
                "oid": str(row.oid),
                "td": row.td
            }
            for row in rows
        ]
