import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from persistance.database import Base
# from persistance.tables import ThingDescriptionDB
from utils import config

# Test database configuration
TEST_DB_NAME = "test_db"
TEST_DATABASE_URL = config.settings.DATABASE_URL.rsplit('/', 1)[0] + f'/{TEST_DB_NAME}'


async def create_test_database():
    """Create the test database if it doesn't exist."""
    # Connect to default 'postgres' database
    default_db_url = config.settings.DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    
    engine_temp = create_async_engine(
        default_db_url,
        isolation_level="AUTOCOMMIT",
        echo=False
    )
    
    try:
        async with engine_temp.connect() as conn:
            # Check if database exists
            result = await conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'")
            )
            exists = result.scalar()
            
            if not exists:
                await conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))
                print(f"✓ Test database '{TEST_DB_NAME}' created successfully")
            else:
                print(f"✓ Test database '{TEST_DB_NAME}' already exists")
    finally:
        await engine_temp.dispose()


async def create_test_tables():
    """Create all tables in test database directly (no Alembic needed)."""
    print("\nCreating tables in test database...")
    
    # Create engine for test database
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    try:
        # Create all tables directly from SQLAlchemy models
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✓ Tables created in test database")
        return True
            
    finally:
        await test_engine.dispose()


async def drop_test_database():
    """Drop the test database (useful for cleanup)."""
    # Connect to default 'postgres' database
    default_db_url = config.settings.DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    
    engine_temp = create_async_engine(
        default_db_url,
        isolation_level="AUTOCOMMIT",
        echo=False
    )
    
    try:
        async with engine_temp.connect() as conn:
            # Terminate existing connections
            await conn.execute(text(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{TEST_DB_NAME}'
                AND pid <> pg_backend_pid()
            """))
            
            # Drop database
            await conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
            print(f"✓ Test database '{TEST_DB_NAME}' dropped successfully")
    finally:
        await engine_temp.dispose()


async def reset_test_database():
    """Drop and recreate test database (fresh state)."""
    print("=" * 60)
    print("RESETTING TEST DATABASE")
    print("=" * 60)
    
    await drop_test_database()
    await create_test_database()
    await create_test_tables()
    
    print("\n" + "=" * 60)
    print("✓ TEST DATABASE RESET COMPLETE")
    print("=" * 60)


async def init_test_db():
    """Initialize test database (create if doesn't exist)."""
    print("=" * 60)
    print("TEST DATABASE INITIALIZATION")
    print("=" * 60)
    
    try:
        await create_test_database()
        await create_test_tables()
        
        print("\n" + "=" * 60)
        print("✓ TEST DATABASE INITIALIZATION COMPLETE")
        print(f"   URL: {TEST_DATABASE_URL}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        # Reset (drop and recreate)
        asyncio.run(reset_test_database())
    elif len(sys.argv) > 1 and sys.argv[1] == "--drop":
        # Just drop
        asyncio.run(drop_test_database())
    else:
        # Initialize (create if not exists)
        asyncio.run(init_test_db())