"""
Initialize all required database tables for the Cement AI system
This script creates all tables needed for the application to work properly.
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import Settings

settings = Settings()


async def create_all_tables(session: AsyncSession):
    """Create all required tables for the application"""
    
    # Kiln Operations Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS kiln_operations (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            kiln_id VARCHAR(50),
            temperature DECIMAL(10, 2),
            feed_rate DECIMAL(10, 2),
            rotation_speed DECIMAL(10, 2),
            pressure DECIMAL(10, 2),
            fuel_consumption DECIMAL(10, 2),
            thermal_efficiency DECIMAL(5, 2),
            production_rate DECIMAL(10, 2),
            status VARCHAR(50),
            location VARCHAR(100),
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """))
    print("✅ kiln_operations table created")
    
    # Alternative Fuels Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS alternative_fuels (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            fuel_type VARCHAR(100),
            quantity_used DECIMAL(10, 2),
            substitution_rate DECIMAL(5, 2),
            cost_savings DECIMAL(10, 2),
            emissions_reduced DECIMAL(10, 2),
            energy_content DECIMAL(10, 2),
            kiln_id VARCHAR(50),
            location VARCHAR(100),
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """))
    print("✅ alternative_fuels table created")
    
    # Grinding Operations Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS grinding_operations (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            mill_id VARCHAR(50),
            feed_rate DECIMAL(10, 2),
            fineness DECIMAL(10, 2),
            power_consumption DECIMAL(10, 2),
            production_rate DECIMAL(10, 2),
            product_type VARCHAR(100),
            location VARCHAR(100),
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """))
    print("✅ grinding_operations table created")
    
    # Quality Control Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS quality_control (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            sample_id VARCHAR(100),
            product_type VARCHAR(100),
            strength_3day DECIMAL(10, 2),
            strength_7day DECIMAL(10, 2),
            strength_28day DECIMAL(10, 2),
            fineness DECIMAL(10, 2),
            cao DECIMAL(5, 2),
            sio2 DECIMAL(5, 2),
            al2o3 DECIMAL(5, 2),
            fe2o3 DECIMAL(5, 2),
            loi DECIMAL(5, 2),
            status VARCHAR(50),
            location VARCHAR(100),
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """))
    print("✅ quality_control table created")
    
    # Raw Material Feed Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS raw_material_feed (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            material_type VARCHAR(100),
            quantity DECIMAL(10, 2),
            source VARCHAR(100),
            quality_grade VARCHAR(50),
            cost_per_ton DECIMAL(10, 2),
            location VARCHAR(100),
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """))
    print("✅ raw_material_feed table created")
    
    # Utilities Monitoring Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS utilities_monitoring (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            utility_type VARCHAR(50),
            consumption DECIMAL(10, 2),
            cost DECIMAL(10, 2),
            unit VARCHAR(20),
            efficiency DECIMAL(5, 2),
            location VARCHAR(100),
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """))
    print("✅ utilities_monitoring table created")
    
    # Optimization Results Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS optimization_results (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            optimization_type VARCHAR(100),
            description TEXT,
            current_value DECIMAL(10, 2),
            optimized_value DECIMAL(10, 2),
            savings DECIMAL(10, 2),
            status VARCHAR(50),
            location VARCHAR(100),
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """))
    print("✅ optimization_results table created")
    
    # AI Recommendations Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS ai_recommendations (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            category VARCHAR(100),
            priority VARCHAR(20),
            title VARCHAR(200),
            description TEXT,
            expected_impact TEXT,
            status VARCHAR(50),
            location VARCHAR(100),
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """))
    print("✅ ai_recommendations table created")
    
    # Chat History Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(100),
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            role VARCHAR(20),
            content TEXT,
            tool_calls JSON,
            meta_data JSON
        )
    """))
    print("✅ chat_history table created")
    
    # Plant Locations Table
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS plant_locations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            city VARCHAR(100),
            state VARCHAR(100),
            country VARCHAR(100) DEFAULT 'India',
            latitude DECIMAL(10, 7),
            longitude DECIMAL(10, 7),
            capacity DECIMAL(10, 2),
            type VARCHAR(50),
            status VARCHAR(50) DEFAULT 'Active',
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        )
    """))
    print("✅ plant_locations table created")
    
    # Create indexes for better performance
    await session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_kiln_operations_timestamp ON kiln_operations(timestamp);
        CREATE INDEX IF NOT EXISTS idx_kiln_operations_location ON kiln_operations(location);
        CREATE INDEX IF NOT EXISTS idx_alternative_fuels_timestamp ON alternative_fuels(timestamp);
        CREATE INDEX IF NOT EXISTS idx_grinding_operations_timestamp ON grinding_operations(timestamp);
        CREATE INDEX IF NOT EXISTS idx_quality_control_timestamp ON quality_control(timestamp);
        CREATE INDEX IF NOT EXISTS idx_raw_material_timestamp ON raw_material_feed(timestamp);
        CREATE INDEX IF NOT EXISTS idx_utilities_timestamp ON utilities_monitoring(timestamp);
        CREATE INDEX IF NOT EXISTS idx_optimization_timestamp ON optimization_results(timestamp);
        CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id);
    """))
    print("✅ Indexes created")
    
    await session.commit()


async def main():
    """Main function to initialize database schema"""
    print("\n" + "="*70)
    print("DATABASE SCHEMA INITIALIZATION - CEMENT AI SYSTEM")
    print("="*70)
    
    # Use database URL from settings (.env file)
    database_url = settings.DATABASE_URL
    
    if not database_url:
        print("\n❌ ERROR: DATABASE_URL not found in environment variables")
        print("Please set DATABASE_URL in your .env file")
        return
    
    print(f"\nConnecting to database: {database_url.split('@')[1] if '@' in database_url else 'database'}...\n")
    
    engine = create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True
    )
    
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    
    try:
        async with async_session_maker() as session:
            print("Creating database tables...\n")
            await create_all_tables(session)
            
            print("\n" + "="*70)
            print("✅ DATABASE SCHEMA INITIALIZATION COMPLETE")
            print("="*70)
            print("\nAll tables have been created successfully!")
            print("You can now run the populate_database.py script to add sample data.\n")
            
    except Exception as e:
        print(f"\n❌ Error during schema initialization: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
