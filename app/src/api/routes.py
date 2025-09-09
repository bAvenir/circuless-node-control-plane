import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from models.thing import ThingDescriptionCreate, ThingDescriptionResponse
from core.crud import ThingDescriptionCRUD

router = APIRouter(
    prefix="/api/v1",
    tags=["WoT Directory"],
    responses={404: {"description": "Not found"}}
)

@router.post("/things/", response_model=ThingDescriptionResponse)
async def create_thing_description(
    td: ThingDescriptionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new Thing Description"""
    td_data = td.dict()
    db_td = await ThingDescriptionCRUD.create(db, td_data)
    return db_td

@router.get("/things/{td_id}", response_model=ThingDescriptionResponse)
async def get_thing_description(
    td_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get Thing Description by ID"""
    db_td = await ThingDescriptionCRUD.get_by_id(db, td_id)
    if not db_td:
        raise HTTPException(status_code=404, detail="Thing Description not found")
    return db_td

@router.get("/things/oid/{oid}", response_model=ThingDescriptionResponse)
async def get_thing_description_by_oid(
    oid: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get Thing Description by OID"""
    db_td = await ThingDescriptionCRUD.get_by_oid(db, oid)
    if not db_td:
        raise HTTPException(status_code=404, detail="Thing Description not found")
    return db_td

@router.get("/things/", response_model=List[ThingDescriptionResponse])
async def list_thing_descriptions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all Thing Descriptions"""
    return await ThingDescriptionCRUD.get_all(db, skip=skip, limit=limit)

@router.put("/things/{td_id}", response_model=ThingDescriptionResponse)
async def update_thing_description(
    td_id: int,
    td: ThingDescriptionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update Thing Description"""
    td_data = td.dict()
    db_td = await ThingDescriptionCRUD.update(db, td_id, td_data)
    if not db_td:
        raise HTTPException(status_code=404, detail="Thing Description not found")
    return db_td

@router.delete("/things/{td_id}")
async def delete_thing_description(
    td_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete Thing Description"""
    success = await ThingDescriptionCRUD.delete(db, td_id)
    if not success:
        raise HTTPException(status_code=404, detail="Thing Description not found")
    return {"message": "Thing Description deleted successfully"}

@router.get("/search/", response_model=List[ThingDescriptionResponse])
async def search_thing_descriptions(
    field: str,
    value: str,
    db: AsyncSession = Depends(get_db)
):
    """Search Thing Descriptions by JSONB field"""
    results = await ThingDescriptionCRUD.query_jsonb_field(db, field, value)
    return results