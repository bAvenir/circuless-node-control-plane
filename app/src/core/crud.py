import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional
from models import thing

class ThingDescriptionCRUD:
    
    @staticmethod
    async def create(db: AsyncSession, td_data: dict) -> thing.ThingDescriptionDB:
        """Create a new Thing Description"""
        db_td = thing.ThingDescriptionDB(
            oid=uuid.uuid4(),
            td=td_data
        )
        db.add(db_td)
        await db.commit()
        await db.refresh(db_td)
        return db_td
    
    @staticmethod
    async def get_by_id(db: AsyncSession, td_id: int) -> Optional[thing.ThingDescriptionDB]:
        """Get Thing Description by ID"""
        result = await db.execute(select(thing.ThingDescriptionDB).filter(thing.ThingDescriptionDB.id == td_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_by_oid(db: AsyncSession, oid: uuid.UUID) -> Optional[thing.ThingDescriptionDB]:
        """Get Thing Description by OID"""
        result = await db.execute(select(thing.ThingDescriptionDB).filter(thing.ThingDescriptionDB.oid == oid))
        return result.scalars().first()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[thing.ThingDescriptionDB]:
        """Get all Thing Descriptions with pagination"""
        result = await db.execute(select(thing.ThingDescriptionDB).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def update(db: AsyncSession, td_id: int, td_data: dict) -> Optional[thing.ThingDescriptionDB]:
        """Update Thing Description"""
        await db.execute(
            update(thing.ThingDescriptionDB)
            .where(thing.ThingDescriptionDB.id == td_id)
            .values(td=td_data)
        )
        await db.commit()
        return await ThingDescriptionCRUD.get_by_id(db, td_id)
    
    @staticmethod
    async def delete(db: AsyncSession, td_id: int) -> bool:
        """Delete Thing Description"""
        result = await db.execute(
            delete(thing.ThingDescriptionDB)
            .where(thing.ThingDescriptionDB.id == td_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def query_jsonb_field(db: AsyncSession, field_path: str, value: any) -> List[thing.ThingDescriptionDB]:
        """Query JSONB field - example: field_path='title', value='MyThing'"""
        result = await db.execute(
            select(thing.ThingDescriptionDB)
            .filter(thing.ThingDescriptionDB.td[field_path].astext == str(value))
        )
        return result.scalars().all()
