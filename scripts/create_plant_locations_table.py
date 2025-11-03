"""
Create plant_locations table in the database
"""
import asyncio
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from app.db.session import AsyncSessionLocal
from app.core.logging_config import logger


async def create_plant_locations_table():
    """Create the plant_locations table"""
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS plant_locations (
        id SERIAL PRIMARY KEY,
        plant_code VARCHAR(50) UNIQUE NOT NULL,
        plant_name VARCHAR(255) NOT NULL,
        location VARCHAR(255),
        city VARCHAR(100),
        state VARCHAR(100),
        country VARCHAR(100),
        latitude FLOAT NOT NULL,
        longitude FLOAT NOT NULL,
        capacity_tpd INTEGER,
        plant_type VARCHAR(100),
        commissioned_year INTEGER,
        status VARCHAR(50) DEFAULT 'operational',
        contact_email VARCHAR(255),
        contact_phone VARCHAR(50),
        description TEXT,
        metadata JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    create_indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_plant_locations_code ON plant_locations(plant_code)",
        "CREATE INDEX IF NOT EXISTS idx_plant_locations_state ON plant_locations(state)",
        "CREATE INDEX IF NOT EXISTS idx_plant_locations_status ON plant_locations(status)",
        "CREATE INDEX IF NOT EXISTS idx_plant_locations_coordinates ON plant_locations(latitude, longitude)"
    ]
    
    async with AsyncSessionLocal() as session:
        try:
            logger.info("Creating plant_locations table...")
            await session.execute(text(create_table_sql))
            
            logger.info("Creating indexes...")
            for idx_sql in create_indexes_sql:
                await session.execute(text(idx_sql))
            
            await session.commit()
            logger.info("✅ plant_locations table and indexes created successfully!")
            return True
        except Exception as e:
            logger.error(f"❌ Error creating plant_locations table: {e}")
            await session.rollback()
            return False


async def main():
    """Main execution function"""
    print("\n" + "=" * 60)
    print("  JK Cement - Create Plant Locations Table")
    print("=" * 60 + "\n")
    
    success = await create_plant_locations_table()
    
    if success:
        print("\n✅ Table created successfully!")
        print("You can now run: python scripts/populate_plant_locations.py")
    else:
        print("\n❌ Failed to create table. Check logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
