"""Quick script to check database data"""
import asyncio
from app.db.session import AsyncSessionLocal
from sqlalchemy import text


async def check_data():
    try:
        async with AsyncSessionLocal() as session:
            # Check kiln_operations
            result = await session.execute(text("SELECT COUNT(*) FROM kiln_operations"))
            kiln_count = result.scalar()
            print(f"✅ Kiln operations records: {kiln_count}")
            
            # Get latest kiln record
            if kiln_count > 0:
                result = await session.execute(text("""
                    SELECT burning_zone_temp, coal_feed_rate, clinker_production, timestamp 
                    FROM kiln_operations 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                """))
                row = result.fetchone()
                if row:
                    print(f"📊 Latest kiln data:")
                    print(f"   - Burning zone temp: {row[0]}")
                    print(f"   - Coal feed rate: {row[1]}")
                    print(f"   - Clinker production: {row[2]}")
                    print(f"   - Timestamp: {row[3]}")
                    
                    # Calculate efficiency with proper type conversion
                    if row[1] and float(row[1]) > 0:
                        efficiency = (float(row[2]) * 1.6) / float(row[1])
                        print(f"   - Calculated efficiency: {efficiency:.2f}")
                        
                # Test the actual efficiency calculation
                print(f"\n🧪 Testing efficiency calculation query:")
                result = await session.execute(text("""
                    SELECT 
                        AVG(burning_zone_temp) as avg_temp,
                        AVG(coal_feed_rate) as avg_coal,
                        AVG(alternative_fuel_rate) as avg_alt_fuel,
                        AVG(clinker_production) as avg_production,
                        AVG(o2_pct) as avg_o2
                    FROM kiln_operations
                    WHERE timestamp >= NOW() - INTERVAL '24 hours'
                """))
                data = result.fetchone()
                if data:
                    avg_temp = float(data[0]) if data[0] else 0
                    avg_coal = float(data[1]) if data[1] else 0
                    avg_alt_fuel = float(data[2]) if data[2] else 0
                    avg_production = float(data[3]) if data[3] else 0
                    avg_o2 = float(data[4]) if data[4] else 0
                    
                    thermal_efficiency = (avg_production * 1.6) / (avg_coal + avg_alt_fuel) if (avg_coal + avg_alt_fuel) > 0 else 0
                    
                    print(f"✅ Efficiency metrics (24h avg):")
                    print(f"   - Avg temperature: {avg_temp:.2f}°C")
                    print(f"   - Avg coal feed: {avg_coal:.2f} t/h")
                    print(f"   - Avg alt fuel: {avg_alt_fuel:.2f} t/h")
                    print(f"   - Avg production: {avg_production:.2f} t/h")
                    print(f"   - Thermal efficiency: {thermal_efficiency:.2f}")
                    print(f"   - Avg O2: {avg_o2:.2f}%")
                    
            else:
                print("❌ No data in kiln_operations table!")
                print("💡 Run: python scripts/populate_database.py")
                
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(check_data())
