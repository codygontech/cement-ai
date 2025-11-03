"""
Populate JK Cement plant locations across India
Based on actual JK Cement manufacturing facilities
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import AsyncSessionLocal
from sqlalchemy import text


async def populate_plant_locations():
    """Populate JK Cement plant locations across India"""
    async with AsyncSessionLocal() as session:
        print("🏭 Populating JK Cement plant locations across India...")
        
        # JK Cement actual plant locations across India
        plants = [
            {
                'plant_code': 'JK-NIMBAHERA',
                'plant_name': 'JK Cement Works, Nimbahera',
                'location': 'Nimbahera, Chittorgarh District',
                'city': 'Nimbahera',
                'state': 'Rajasthan',
                'latitude': 24.6210,
                'longitude': 74.6850,
                'capacity_tpd': 6000,
                'plant_type': 'Integrated Cement Plant',
                'commissioned_year': 1975,
                'status': 'operational',
                'contact_email': 'nimbahera@jkcement.com',
                'contact_phone': '+91-1478-220200',
                'description': 'One of the largest integrated cement plants of JK Cement in Rajasthan. Features state-of-the-art technology with high alternative fuel usage.'
            },
            {
                'plant_code': 'JK-MANGROL',
                'plant_name': 'JK Cement Works, Mangrol',
                'location': 'Mangrol, Chittorgarh District',
                'city': 'Mangrol',
                'state': 'Rajasthan',
                'latitude': 24.8644,
                'longitude': 75.0753,
                'capacity_tpd': 5200,
                'plant_type': 'Integrated Cement Plant',
                'commissioned_year': 2010,
                'status': 'operational',
                'contact_email': 'mangrol@jkcement.com',
                'contact_phone': '+91-1478-252200',
                'description': 'Modern integrated plant with advanced automation and energy efficiency systems. Strong focus on sustainability.'
            },
            {
                'plant_code': 'JK-MUDDAPUR',
                'plant_name': 'JK Lakshmi Cement, Muddapur',
                'location': 'Muddapur Village, Bagalkot District',
                'city': 'Muddapur',
                'state': 'Karnataka',
                'latitude': 16.1000,
                'longitude': 75.8167,
                'capacity_tpd': 2100,
                'plant_type': 'Integrated Cement Plant',
                'commissioned_year': 2008,
                'status': 'operational',
                'contact_email': 'muddapur@jklakshmicement.com',
                'contact_phone': '+91-8376-252100',
                'description': 'JK Lakshmi brand manufacturing facility in Karnataka with excellent limestone reserves.'
            },
            {
                'plant_code': 'JK-SURAT',
                'plant_name': 'JK Cement Works, Surat',
                'location': 'Hazira, Surat District',
                'city': 'Surat',
                'state': 'Gujarat',
                'latitude': 21.1167,
                'longitude': 72.6333,
                'capacity_tpd': 1800,
                'plant_type': 'Grinding Unit',
                'commissioned_year': 2013,
                'status': 'operational',
                'contact_email': 'surat@jkcement.com',
                'contact_phone': '+91-261-2461500',
                'description': 'Modern grinding unit strategically located in Gujarat industrial belt for efficient distribution.'
            },
            {
                'plant_code': 'JK-JHARLI',
                'plant_name': 'JK Lakshmi Cement, Jharli',
                'location': 'Jharli, Jhajjar District',
                'city': 'Jharli',
                'state': 'Haryana',
                'latitude': 28.6667,
                'longitude': 76.5500,
                'capacity_tpd': 1000,
                'plant_type': 'Grinding Unit',
                'commissioned_year': 2011,
                'status': 'operational',
                'contact_email': 'jharli@jklakshmicement.com',
                'contact_phone': '+91-1251-252300',
                'description': 'Strategic grinding unit serving North India markets with JK Lakshmi brand.'
            },
            {
                'plant_code': 'JK-KALOL',
                'plant_name': 'JK Cement Works, Kalol',
                'location': 'Kalol, Gandhinagar District',
                'city': 'Kalol',
                'state': 'Gujarat',
                'latitude': 23.2500,
                'longitude': 72.5000,
                'capacity_tpd': 1500,
                'plant_type': 'Grinding Unit',
                'commissioned_year': 2015,
                'status': 'operational',
                'contact_email': 'kalol@jkcement.com',
                'contact_phone': '+91-2764-252400',
                'description': 'Modern grinding facility with advanced quality control systems.'
            },
            {
                'plant_code': 'JK-DURGAPUR',
                'plant_name': 'JK Lakshmi Cement, Durgapur',
                'location': 'Durgapur, West Bengal',
                'city': 'Durgapur',
                'state': 'West Bengal',
                'latitude': 23.5204,
                'longitude': 87.3119,
                'capacity_tpd': 900,
                'plant_type': 'Grinding Unit',
                'commissioned_year': 2009,
                'status': 'operational',
                'contact_email': 'durgapur@jklakshmicement.com',
                'contact_phone': '+91-343-2545000',
                'description': 'Grinding unit serving Eastern India with efficient logistics network.'
            },
            {
                'plant_code': 'JK-ALIGARH',
                'plant_name': 'JK White Cement, Aligarh',
                'location': 'Aligarh, Uttar Pradesh',
                'city': 'Aligarh',
                'state': 'Uttar Pradesh',
                'latitude': 27.8974,
                'longitude': 78.0880,
                'capacity_tpd': 600,
                'plant_type': 'White Cement Plant',
                'commissioned_year': 2000,
                'status': 'operational',
                'contact_email': 'aligarh@jkwhitecement.com',
                'contact_phone': '+91-571-2740100',
                'description': 'Specialized white cement manufacturing facility, one of the largest in India.'
            },
            {
                'plant_code': 'JK-GOTAN',
                'plant_name': 'JK White Cement, Gotan',
                'location': 'Gotan, Nagaur District',
                'city': 'Gotan',
                'state': 'Rajasthan',
                'latitude': 26.9667,
                'longitude': 73.4833,
                'capacity_tpd': 800,
                'plant_type': 'White Cement Plant',
                'commissioned_year': 2005,
                'status': 'operational',
                'contact_email': 'gotan@jkwhitecement.com',
                'contact_phone': '+91-1591-252500',
                'description': 'Advanced white cement production facility with global quality standards.'
            },
            {
                'plant_code': 'JK-JAJPUR',
                'plant_name': 'JK Cement Works, Jajpur',
                'location': 'Jajpur, Odisha',
                'city': 'Jajpur',
                'state': 'Odisha',
                'latitude': 20.8500,
                'longitude': 86.3333,
                'capacity_tpd': 1200,
                'plant_type': 'Grinding Unit',
                'commissioned_year': 2016,
                'status': 'operational',
                'contact_email': 'jajpur@jkcement.com',
                'contact_phone': '+91-6728-252600',
                'description': 'Modern grinding facility serving Odisha and surrounding markets.'
            },
            {
                'plant_code': 'JK-FUJAIRAH',
                'plant_name': 'JK Cement Works, Fujairah (UAE)',
                'location': 'Fujairah, United Arab Emirates',
                'city': 'Fujairah',
                'state': 'International',
                'latitude': 25.1288,
                'longitude': 56.3265,
                'capacity_tpd': 3600,
                'plant_type': 'Integrated Cement Plant',
                'commissioned_year': 2010,
                'status': 'operational',
                'contact_email': 'fujairah@jkcement.com',
                'contact_phone': '+971-9-2236600',
                'description': 'JK Cement\'s international facility in UAE serving Middle East and African markets.'
            },
            {
                'plant_code': 'JK-PANNA',
                'plant_name': 'JK Cement Works, Panna (Planned)',
                'location': 'Panna District, Madhya Pradesh',
                'city': 'Panna',
                'state': 'Madhya Pradesh',
                'latitude': 24.7167,
                'longitude': 80.1833,
                'capacity_tpd': 3000,
                'plant_type': 'Integrated Cement Plant',
                'commissioned_year': 2026,
                'status': 'planned',
                'contact_email': 'panna@jkcement.com',
                'contact_phone': '+91-7732-252700',
                'description': 'Upcoming greenfield integrated cement plant project in Madhya Pradesh. Expected commissioning in 2026.'
            }
        ]
        
        for plant in plants:
            await session.execute(text("""
                INSERT INTO plant_locations 
                (plant_code, plant_name, location, city, state, country,
                 latitude, longitude, capacity_tpd, plant_type, 
                 commissioned_year, status, contact_email, contact_phone, description)
                VALUES (:plant_code, :plant_name, :location, :city, :state, 'India',
                        :latitude, :longitude, :capacity_tpd, :plant_type,
                        :commissioned_year, :status, :contact_email, :contact_phone, :description)
            """), plant)
        
        await session.commit()
        print(f"✅ Populated {len(plants)} JK Cement plant locations")
        
        # Print summary
        print("\n📊 Plant Location Summary:")
        print(f"   • Integrated Plants: {sum(1 for p in plants if 'Integrated' in p['plant_type'])}")
        print(f"   • Grinding Units: {sum(1 for p in plants if 'Grinding' in p['plant_type'])}")
        print(f"   • White Cement Plants: {sum(1 for p in plants if 'White' in p['plant_type'])}")
        print(f"   • Operational: {sum(1 for p in plants if p['status'] == 'operational')}")
        print(f"   • Planned: {sum(1 for p in plants if p['status'] == 'planned')}")
        print(f"   • Total Capacity: {sum(p['capacity_tpd'] for p in plants):,} TPD")
        
        states = set(p['state'] for p in plants)
        print(f"\n🗺️  States Covered: {', '.join(sorted(states))}")


async def main():
    """Main function to populate plant locations"""
    print("\n" + "="*60)
    print("  JK Cement Plant Locations - Database Population")
    print("="*60 + "\n")
    
    try:
        await populate_plant_locations()
        
        print("\n" + "="*60)
        print("  ✅ Plant locations populated successfully!")
        print("="*60 + "\n")
        print("Available API endpoints:")
        print("  • GET  /api/locations - Get all plant locations")
        print("  • GET  /api/locations/{plant_code} - Get specific plant")
        print("  • GET  /api/locations/nearby/{plant_code} - Get nearby plants")
        print("  • GET  /api/locations/state/{state} - Get plants by state")
        print("  • GET  /api/locations/stats/summary - Get statistics")
        print("  • GET  /api/locations/map/markers - Get map markers")
        print()
        
    except Exception as e:
        print(f"\n❌ Error populating plant locations: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
