from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from persistance.tables import Dataset


async def get_dataset(db: AsyncSession, dataset_id: str):
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    return result.scalar_one_or_none()


async def create_dataset(db: AsyncSession, dataset_id: str, dataset_data: dict):
    new_dataset = Dataset(id=dataset_id, dataset_data=dataset_data)
    db.add(new_dataset)
    await db.commit()
    await db.refresh(new_dataset)
    return new_dataset


async def get_all_datasets(db: AsyncSession):
    result = await db.execute(select(Dataset))
    return result.scalars().all()
