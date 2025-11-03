"""
Script to check for duplicate content in the database
"""
import asyncio
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import Settings
from app.core.database import (
    RawMaterialFeed, 
    KilnOperations, 
    GrindingOperations, 
    QualityControl,
    AIRecommendations,
    ChatHistory
)

settings = Settings()


async def check_table_duplicates(session: AsyncSession, table_class, group_by_columns: list):
    """Check for duplicates in a specific table"""
    table_name = table_class.__tablename__
    print(f"\n{'='*60}")
    print(f"Checking {table_name} for duplicates...")
    print(f"{'='*60}")
    
    try:
        # Get total count
        total_result = await session.execute(select(func.count(table_class.id)))
        total_count = total_result.scalar()
        print(f"Total records: {total_count}")
        
        if total_count == 0:
            print(f"No records in {table_name}")
            return
    except Exception as e:
        await session.rollback()  # Rollback on error
        if "does not exist" in str(e):
            print(f"⚠️  Table {table_name} does not exist in database - skipping")
            return
        raise
    
    # Build query to find duplicates
    group_cols = [getattr(table_class, col) for col in group_by_columns]
    
    # Count duplicates by grouping
    stmt = (
        select(*group_cols, func.count(table_class.id).label('count'))
        .group_by(*group_cols)
        .having(func.count(table_class.id) > 1)
    )
    
    result = await session.execute(stmt)
    duplicates = result.fetchall()
    
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} groups of duplicates:")
        for i, dup in enumerate(duplicates[:10], 1):  # Show first 10
            count = dup[-1]
            values = dup[:-1]
            print(f"  {i}. {dict(zip(group_by_columns, values))} - {count} duplicates")
        
        if len(duplicates) > 10:
            print(f"  ... and {len(duplicates) - 10} more duplicate groups")
        
        # Get detailed info for first duplicate group
        first_dup = duplicates[0]
        conditions = [getattr(table_class, col) == val for col, val in zip(group_by_columns, first_dup[:-1])]
        detail_stmt = select(table_class).where(and_(*conditions))
        detail_result = await session.execute(detail_stmt)
        detail_records = detail_result.scalars().all()
        
        print(f"\n  Details of first duplicate group ({len(detail_records)} records):")
        for record in detail_records:
            print(f"    ID: {record.id}, Timestamp: {record.timestamp}")
    else:
        print(f"✓ No duplicates found based on {', '.join(group_by_columns)}")


async def check_exact_duplicates(session: AsyncSession, table_class):
    """Check for exact duplicate rows (excluding id and timestamp)"""
    table_name = table_class.__tablename__
    print(f"\n  Checking for exact row duplicates in {table_name}...")
    
    # This would require comparing all columns except id and timestamp
    # For now, we'll skip this complex check and focus on key field duplicates
    print(f"  (Exact row duplicate check skipped - focus on key fields)")


async def main():
    """Main function to check all tables for duplicates"""
    print("\n" + "="*60)
    print("DATABASE DUPLICATE CONTENT CHECKER")
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
            # Check RawMaterialFeed - duplicates by timestamp
            await check_table_duplicates(
                session, 
                RawMaterialFeed, 
                ['timestamp']
            )
            
            # Check KilnOperations - duplicates by timestamp
            await check_table_duplicates(
                session, 
                KilnOperations, 
                ['timestamp']
            )
            
            # Check GrindingOperations - duplicates by timestamp only (mill_type doesn't exist in DB)
            await check_table_duplicates(
                session, 
                GrindingOperations, 
                ['timestamp']
            )
            
            # Check QualityControl - duplicates by sample_type
            await check_table_duplicates(
                session, 
                QualityControl, 
                ['sample_type']
            )
            
            # Check AIRecommendations - duplicates by timestamp only (module column doesn't exist)
            await check_table_duplicates(
                session, 
                AIRecommendations, 
                ['timestamp']
            )
            
            # Check ChatHistory - duplicates by session_id, timestamp, content
            await check_table_duplicates(
                session, 
                ChatHistory, 
                ['session_id', 'timestamp', 'content']
            )
            
            print("\n" + "="*60)
            print("DUPLICATE CHECK COMPLETE")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"\n❌ Error checking database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
