"""
Test script to verify database connectivity fix
Tests the Cloud SQL connector event loop issue is resolved
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings
from app.db import session as db_session
from app.core.logging_config import logger


async def test_engine_initialization():
    """Test 1: Verify engine initializes properly"""
    print("\n" + "="*60)
    print("TEST 1: Engine Initialization")
    print("="*60)
    
    try:
        await db_session.init_engine()
        
        if db_session.engine:
            print("✓ Database engine initialized successfully")
            return True
        else:
            print("✗ Engine initialization returned None")
            return False
    except Exception as e:
        print(f"✗ Engine initialization failed: {e}")
        return False


async def test_database_connection():
    """Test 2: Verify database connection works"""
    print("\n" + "="*60)
    print("TEST 2: Database Connection")
    print("="*60)
    
    if not db_session.engine:
        print("✗ Database engine not configured")
        return False
    
    try:
        from sqlalchemy import text
        
        async with db_session.engine.connect() as conn:
            result = await conn.execute(text("SELECT 1 as test"))
            row = await result.fetchone()
            
            if row and row[0] == 1:
                print("✓ Database connection successful")
                print(f"✓ Query result: {row[0]}")
                return True
            else:
                print("✗ Unexpected query result")
                return False
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


async def test_session_creation():
    """Test 3: Verify session creation works"""
    print("\n" + "="*60)
    print("TEST 3: Session Creation")
    print("="*60)
    
    if not db_session.AsyncSessionLocal:
        print("✗ AsyncSessionLocal not configured")
        return False
    
    try:
        async with db_session.AsyncSessionLocal() as session:
            from sqlalchemy import text
            result = await session.execute(text("SELECT current_database(), version()"))
            row = await result.fetchone()
            
            if row:
                print(f"✓ Session created successfully")
                print(f"✓ Database: {row[0]}")
                print(f"✓ Version: {row[1][:50]}...")
                return True
            else:
                print("✗ No result from session query")
                return False
    except Exception as e:
        print(f"✗ Session creation failed: {e}")
        return False


async def test_multiple_connections():
    """Test 4: Verify multiple connections work (event loop test)"""
    print("\n" + "="*60)
    print("TEST 4: Multiple Concurrent Connections")
    print("="*60)
    
    if not db_session.AsyncSessionLocal:
        print("✗ AsyncSessionLocal not configured")
        return False
    
    try:
        async def query_db(n):
            async with db_session.AsyncSessionLocal() as session:
                from sqlalchemy import text
                result = await session.execute(text(f"SELECT {n} as num"))
                row = await result.fetchone()
                return row[0]
        
        # Run 5 concurrent queries
        tasks = [query_db(i) for i in range(1, 6)]
        results = await asyncio.gather(*tasks)
        
        if results == [1, 2, 3, 4, 5]:
            print(f"✓ All {len(results)} concurrent connections successful")
            print(f"✓ Results: {results}")
            return True
        else:
            print(f"✗ Unexpected results: {results}")
            return False
    except Exception as e:
        print(f"✗ Multiple connections failed: {e}")
        return False


async def test_table_list():
    """Test 5: List database tables"""
    print("\n" + "="*60)
    print("TEST 5: Table Listing")
    print("="*60)
    
    if not db_session.AsyncSessionLocal:
        print("✗ AsyncSessionLocal not configured")
        return False
    
    try:
        async with db_session.AsyncSessionLocal() as session:
            from sqlalchemy import text
            result = await session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in await result.fetchall()]
            
            if tables:
                print(f"✓ Found {len(tables)} tables:")
                for table in tables:
                    print(f"  • {table}")
                return True
            else:
                print("ℹ No tables found (database might be empty)")
                return True
    except Exception as e:
        print(f"✗ Table listing failed: {e}")
        return False


async def test_cleanup():
    """Test 6: Verify proper cleanup"""
    print("\n" + "="*60)
    print("TEST 6: Connector Cleanup")
    print("="*60)
    
    try:
        await db_session.cleanup_connector()
        print("✓ Connector cleanup successful")
        return True
    except Exception as e:
        print(f"✗ Connector cleanup failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("DATABASE CONNECTIVITY TEST SUITE")
    print("="*60)
    print(f"Project: {settings.GOOGLE_CLOUD_PROJECT}")
    print(f"USE_CLOUD_SQL_PROXY: {settings.USE_CLOUD_SQL_PROXY}")
    
    if settings.USE_CLOUD_SQL_PROXY:
        print(f"DATABASE_URL: {settings.DATABASE_URL[:30]}..." if settings.DATABASE_URL else "Not set")
    else:
        print(f"JDBC_DB_STRING: {settings.JDBC_DB_STRING[:50]}..." if settings.JDBC_DB_STRING else "Not set")
    
    results = []
    
    # Run tests
    results.append(("Engine Initialization", await test_engine_initialization()))
    results.append(("Database Connection", await test_database_connection()))
    results.append(("Session Creation", await test_session_creation()))
    results.append(("Multiple Connections", await test_multiple_connections()))
    results.append(("Table Listing", await test_table_list()))
    results.append(("Connector Cleanup", await test_cleanup()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! Database connectivity is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
