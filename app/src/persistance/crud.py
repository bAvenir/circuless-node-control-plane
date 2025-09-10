import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional
from persistance import models

class ThingDescriptionCRUD:
    
    @staticmethod
    async def create(db: AsyncSession, td_data: dict) -> models.ThingDescriptionDB:
        """Create a new Thing Description"""
        oid=uuid.uuid4()
        td=td_data
        td['oid']=str(oid)
        db_td = models.ThingDescriptionDB(
            oid=oid,
            td=td
        )
        db.add(db_td)
        await db.commit()
        await db.refresh(db_td)
        return db_td
    
    @staticmethod
    async def get_by_id(db: AsyncSession, td_id: int) -> Optional[models.ThingDescriptionDB]:
        """Get Thing Description by ID"""
        result = await db.execute(select(models.ThingDescriptionDB).filter(models.ThingDescriptionDB.id == td_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_by_oid(db: AsyncSession, oid: uuid.UUID) -> Optional[models.ThingDescriptionDB]:
        """Get Thing Description by OID"""
        result = await db.execute(select(models.ThingDescriptionDB).filter(models.ThingDescriptionDB.oid == oid))
        return result.scalars().first()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.ThingDescriptionDB]:
        """Get all Thing Descriptions with pagination"""
        result = await db.execute(select(models.ThingDescriptionDB).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def update(db: AsyncSession, td_id: int, td_data: dict) -> Optional[models.ThingDescriptionDB]:
        """Update Thing Description"""
        await db.execute(
            update(models.ThingDescriptionDB)
            .where(models.ThingDescriptionDB.id == td_id)
            .values(td=td_data)
        )
        await db.commit()
        return await ThingDescriptionCRUD.get_by_id(db, td_id)
    
    @staticmethod
    async def delete(db: AsyncSession, td_id: int) -> bool:
        """Delete Thing Description"""
        result = await db.execute(
            delete(models.ThingDescriptionDB)
            .where(models.ThingDescriptionDB.id == td_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def query_jsonb_field(db: AsyncSession, field_path: str, value: any) -> List[models.ThingDescriptionDB]:
        """Query JSONB field - example: field_path='title', value='MyThing'"""
        result = await db.execute(
            select(models.ThingDescriptionDB)
            .filter(models.ThingDescriptionDB.td[field_path].astext == str(value))
        )
        return result.scalars().all()
