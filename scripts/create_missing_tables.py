"""
Create missing chat_history table in the database
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


async def create_chat_history_table(session: AsyncSession):
    """Create the chat_history table"""
    
    create_table_sql = text("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(100),
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
            role VARCHAR(20),
            content TEXT,
            tool_calls JSON,
            meta_data JSON
        )
    """)
    
    create_index_sql = text("""
        CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id)
    """)
    
    await session.execute(create_table_sql)
    await session.execute(create_index_sql)
    await session.commit()
    print("✅ chat_history table created successfully")


async def main():
    """Main function to create missing tables"""
    print("\n" + "="*60)
    print("DATABASE MIGRATION - CREATE MISSING TABLES")
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
            print("Creating missing tables...")
            await create_chat_history_table(session)
            
            print("\n" + "="*60)
            print("MIGRATION COMPLETE")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
