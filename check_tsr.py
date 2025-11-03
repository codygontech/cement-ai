"""Quick check for TSR data"""
import asyncio
from app.db.session import AsyncSessionLocal
from sqlalchemy import text


async def check_tsr():
    async with AsyncSessionLocal() as session:
        # Check alternative_fuels table
        result = await session.execute(text("""
            SELECT fuel_type, tsr, timestamp 
            FROM alternative_fuels 
            ORDER BY timestamp DESC 
            LIMIT 10
        """))
        rows = result.fetchall()
        
        print("\n📊 Recent alternative_fuels records:")
        print("-" * 60)
        if rows:
            for row in rows:
                print(f"  {row[0]:<20} TSR: {row[1]:>6.2f}%  at {row[2]}")
            
            # Calculate average
            result2 = await session.execute(text("""
                SELECT AVG(tsr) as avg_tsr, COUNT(*) as count
                FROM alternative_fuels
            """))
            avg_row = result2.fetchone()
            print("-" * 60)
            print(f"  Average TSR: {avg_row[0]:.2f}% ({avg_row[1]} records)")
        else:
            print("  ❌ No data found in alternative_fuels table!")
        
        # Check what the API endpoint returns
        print("\n🔍 Checking API query:")
        result3 = await session.execute(text("""
            SELECT * FROM alternative_fuels
            ORDER BY timestamp DESC
            LIMIT 3
        """))
        api_rows = result3.fetchall()
        columns = result3.keys()
        
        print(f"  Columns: {', '.join(columns)}")
        if api_rows:
            print(f"  Sample record fields:")
            for i, col in enumerate(columns):
                print(f"    {col}: {api_rows[0][i]}")


if __name__ == "__main__":
    asyncio.run(check_tsr())
