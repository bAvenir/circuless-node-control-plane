import sys
import asyncio
import json
from pathlib import Path
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = PROJECT_ROOT.parent / "samples/sample_tds"

from persistance.database import AsyncSessionLocal
from persistance.tables import ThingDescriptionDB

async def load_samples():
    async with AsyncSessionLocal() as db:
        # Print all sample files
        sample_files = list(SAMPLES_DIR.glob("*.json"))
        print("Found sample files:", sample_files)

        # Add sample files
        for file in sample_files:
            data = json.loads(file.read_text())
            item = ThingDescriptionDB(td=data)
            db.add(item)
            print("Adding item:", data)

        await db.commit()
        print("All samples committed")

        # Verify
        result = await db.execute(text("SELECT id, td FROM thing_descriptions"))
        rows = result.fetchall()
        print(f"Rows now in table ({len(rows)}):")
        for row in rows:
            print(row)


if __name__ == "__main__":
    asyncio.run(load_samples())
