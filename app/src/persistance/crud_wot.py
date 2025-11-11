import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional
from persistance import models_wot

URN = "urn:circ:<org>:wot:<uuid>"

class ThingDescriptionCRUD:
    
    @staticmethod
    async def create(db: AsyncSession, td_data: dict) -> models_wot.ThingDescriptionDB:
        """Create a new Thing Description"""

        oid=uuid.uuid4()
        td=td_data
        td['oid']=str(oid)
        db_td = models_wot.ThingDescriptionDB(
            oid=oid,
            td=td
        )
        db.add(db_td)
        await db.commit()
        await db.refresh(db_td)
        return db_td
    
    @staticmethod
    async def get_by_id(db: AsyncSession, td_id: int) -> Optional[models_wot.ThingDescriptionDB]:
        """Get Thing Description by ID"""
        result = await db.execute(select(models_wot.ThingDescriptionDB).filter(models_wot.ThingDescriptionDB.id == td_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_by_oid(db: AsyncSession, oid: uuid.UUID) -> Optional[models_wot.ThingDescriptionDB]:
        """Get Thing Description by OID"""
        result = await db.execute(select(models_wot.ThingDescriptionDB).filter(models_wot.ThingDescriptionDB.oid == oid))
        return result.scalars().first()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models_wot.ThingDescriptionDB]:
        """Get all Thing Descriptions with pagination"""
        result = await db.execute(select(models_wot.ThingDescriptionDB).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def update(db: AsyncSession, td_id: int, td_data: dict) -> Optional[models_wot.ThingDescriptionDB]:
        """Update Thing Description"""
        await db.execute(
            update(models_wot.ThingDescriptionDB)
            .where(models_wot.ThingDescriptionDB.id == td_id)
            .values(td=td_data)
        )
        await db.commit()
        return await ThingDescriptionCRUD.get_by_id(db, td_id)
    
    @staticmethod
    async def delete(db: AsyncSession, td_id: int) -> bool:
        """Delete Thing Description"""
        result = await db.execute(
            delete(models_wot.ThingDescriptionDB)
            .where(models_wot.ThingDescriptionDB.id == td_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def query_jsonb_field(db: AsyncSession, field_path: str, value: any) -> List[models_wot.ThingDescriptionDB]:
        """Query JSONB field - example: field_path='title', value='MyThing'"""
        result = await db.execute(
            select(models_wot.ThingDescriptionDB)
            .filter(models_wot.ThingDescriptionDB.td[field_path].astext == str(value))
        )
        return result.scalars().all()
