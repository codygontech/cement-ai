"""
Script to check the actual database schema
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


async def get_table_schema(session: AsyncSession, table_name: str):
    """Get column information for a table"""
    query = text("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = :table_name
        ORDER BY ordinal_position;
    """)
    
    result = await session.execute(query, {"table_name": table_name})
    return result.fetchall()


async def get_all_tables(session: AsyncSession):
    """Get all tables in the database"""
    query = text("""
        SELECT tablename 
        FROM pg_catalog.pg_tables 
        WHERE schemaname = 'public'
        ORDER BY tablename;
    """)
    
    result = await session.execute(query)
    return [row[0] for row in result.fetchall()]


async def main():
    """Main function to check database schema"""
    print("\n" + "="*60)
    print("DATABASE SCHEMA CHECKER")
    print("="*60)
    
    # Use database URL from settings (.env file)
    database_url = settings.DATABASE_URL
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
            # Get all tables
            tables = await get_all_tables(session)
            
            print(f"Found {len(tables)} tables in database:\n")
            
            for table in tables:
                print(f"\n{'='*60}")
                print(f"Table: {table}")
                print(f"{'='*60}")
                
                columns = await get_table_schema(session, table)
                
                if columns:
                    print(f"{'Column':<30} {'Type':<20} {'Nullable':<10} {'Default'}")
                    print("-" * 80)
                    for col in columns:
                        col_name, data_type, nullable, default = col
                        default_str = str(default)[:20] if default else ""
                        print(f"{col_name:<30} {data_type:<20} {nullable:<10} {default_str}")
                else:
                    print("No columns found")
            
            print("\n" + "="*60)
            print("SCHEMA CHECK COMPLETE")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"\n❌ Error checking schema: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
