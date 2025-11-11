import asyncio
import subprocess
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from persistance.database import engine, Base
from persistance.models_wot import ThingDescriptionDB  # Import ALL your models here
from utils import config

settings = config.settings


async def create_database():
    """Create the database if it doesn't exist."""
    # Extract database name from URL
    db_name = settings.DATABASE_URL.rsplit('/', 1)[1].split('?')[0]  # Handle query params
    
    # Connect to default 'postgres' database
    default_db_url = settings.DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    
    engine_temp = create_async_engine(
        default_db_url,
        isolation_level="AUTOCOMMIT",
        echo=True
    )
    
    try:
        async with engine_temp.connect() as conn:
            # Check if database exists
            result = await conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            )
            exists = result.scalar()
            
            if not exists:
                await conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"✓ Database '{db_name}' created successfully")
            else:
                print(f"✓ Database '{db_name}' already exists")
    finally:
        await engine_temp.dispose()


async def create_tables():
    """Create all tables defined in models."""
    print("\nCreating tables...")
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✓ All tables created successfully")


async def init_alembic():
    """Initialize Alembic and create initial migration."""
    print("\nInitializing Alembic...")
    
    # Check if alembic is already initialized
    import os
    if not os.path.exists("alembic"):
        print("Initializing Alembic for the first time...")
        result = subprocess.run(["alembic", "init", "alembic"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Alembic initialized")
            print("\n⚠️  IMPORTANT: Please update alembic/env.py with your configuration")
            print("   Then run this script again.")
            return False
        else:
            print("✗ Alembic initialization failed")
            print(result.stderr)
            return False
    
    # Stamp the database with the current state
    print("Stamping database with current state...")
    result = subprocess.run(["alembic", "stamp", "head"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Database stamped successfully")
        print(result.stdout)
        return True
    else:
        # If no migrations exist, create initial migration
        print("Creating initial migration...")
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", "Initial migration"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Initial migration created")
            print(result.stdout)
            
            # Apply the migration
            result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Migration applied successfully")
                return True
            else:
                print("✗ Migration failed")
                print(result.stderr)
                return False
        else:
            print("✗ Failed to create migration")
            print(result.stderr)
            return False


async def init_db():
    """Complete database initialization."""
    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)
    
    try:
        # Step 1: Create database
        await create_database()
        
        # Step 2: Create tables
        await create_tables()
        
        # Step 3: Initialize Alembic
        await init_alembic()
        
        print("\n" + "=" * 60)
        print("✓ DATABASE INITIALIZATION COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())