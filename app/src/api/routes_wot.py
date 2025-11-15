import uuid
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from persistance.database import get_db
from persistance.models_wot import ThingDescriptionCreate, ThingDescriptionResponse
from persistance.crud_wot import ThingDescriptionCRUD

logger = logging.getLogger(__name__)

router_wot = APIRouter(
    prefix="/things",
    tags=["WoT Directory"],
    responses={404: {"description": "Not found"}}
)

@router_wot.post("/", response_model=ThingDescriptionResponse)
async def create_thing_description(
    td: ThingDescriptionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new Thing Description"""
    td_data = td.dict()
    db_td = await ThingDescriptionCRUD.create(db, td_data)
    logger.info("Asset succesfuly posted")
    return db_td

@router_wot.get("/{td_id}", response_model=ThingDescriptionResponse)
async def get_thing_description(
    td_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get Thing Description by ID"""
    db_td = await ThingDescriptionCRUD.get_by_id(db, td_id)
    if not db_td:
        raise HTTPException(status_code=404, detail="Thing Description not found")
    logger.info("Asset succesfuly retrieved")
    return db_td

@router_wot.get("/oid/{oid}", response_model=ThingDescriptionResponse)
async def get_thing_description_by_oid(
    oid: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get Thing Description by OID"""
    db_td = await ThingDescriptionCRUD.get_by_oid(db, oid)
    if not db_td:
        raise HTTPException(status_code=404, detail="Thing Description not found")
    logger.info("Asset succesfuly retrieved")
    return db_td

@router_wot.get("/", response_model=List[ThingDescriptionResponse])
async def list_thing_descriptions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all Thing Descriptions"""
    logger.info("Assets succesfuly retrieved")
    return await ThingDescriptionCRUD.get_all(db, skip=skip, limit=limit)

@router_wot.put("/{td_id}", response_model=ThingDescriptionResponse)
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
    logger.info("Asset succesfuly updated")
    return db_td

@router_wot.delete("/{td_id}")
async def delete_thing_description(
    td_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete Thing Description"""
    success = await ThingDescriptionCRUD.delete(db, td_id)
    if not success:
        raise HTTPException(status_code=404, detail="Thing Description not found")
    logger.info("Asset succesfuly deleted")
    return {"message": "Thing Description deleted successfully"}

@router_wot.get("/search/jsonpath", response_model=List[ThingDescriptionResponse])
async def search_thing_descriptions(
    query: str,
    db: AsyncSession = Depends(get_db)
):
    """Search Thing Descriptions by JSONB query"""
    results = await ThingDescriptionCRUD.jsonpath_query(db, query)
    logger.info("Asset succesfuly retrieved")
    return results