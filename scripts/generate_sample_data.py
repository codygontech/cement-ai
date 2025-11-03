"""
Sample data generator for JK Cement AI Optimization System
Generates realistic plant operation data for JK Cement India facilities
"""

import asyncio
from datetime import datetime, timedelta
import random
from sqlalchemy import text
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import AsyncSessionLocal
from app.core.logging_config import logger


async def generate_kiln_data(hours=24):
    """Generate sample kiln operations data"""
    async with AsyncSessionLocal() as session:
        logger.info(f"Generating {hours} hours of kiln operations data...")
        
        for i in range(hours):
            timestamp = datetime.now() - timedelta(hours=hours-i)
            
            # Realistic kiln parameters with some variation
            feed_rate = 100 + random.uniform(-5, 5)
            coal_rate = 10 + random.uniform(-1, 1)
            alt_fuel_rate = 3 + random.uniform(-0.5, 0.5)
            temp = 1450 + random.uniform(-20, 20)
            
            await session.execute(text("""
                INSERT INTO kiln_operations 
                (timestamp, feed_rate, kiln_speed, burning_zone_temp, 
                 coal_feed_rate, alternative_fuel_rate, o2_pct, 
                 co_ppm, nox_ppm, clinker_production)
                VALUES (:ts, :feed, :speed, :temp, :coal, :alt_fuel, 
                        :o2, :co, :nox, :clinker)
            """), {
                'ts': timestamp,
                'feed': feed_rate,
                'speed': 3.5 + random.uniform(-0.2, 0.2),
                'temp': temp,
                'coal': coal_rate,
                'alt_fuel': alt_fuel_rate,
                'o2': 3.5 + random.uniform(-0.5, 0.5),
                'co': 50 + random.uniform(-10, 10),
                'nox': 800 + random.uniform(-50, 50),
                'clinker': feed_rate * 0.9 + random.uniform(-2, 2)
            })
        
        await session.commit()
        logger.info(f"✓ Generated {hours} kiln operations records")


async def generate_grinding_data(hours=24):
    """Generate sample grinding operations data"""
    async with AsyncSessionLocal() as session:
        logger.info(f"Generating {hours} hours of grinding operations data...")
        
        for i in range(hours):
            timestamp = datetime.now() - timedelta(hours=hours-i)
            
            feed_rate = 80 + random.uniform(-5, 5)
            power = feed_rate * 35 + random.uniform(-50, 50)
            
            await session.execute(text("""
                INSERT INTO grinding_operations 
                (timestamp, mill_type, feed_rate, mill_speed, power_consumption,
                 differential_pressure, separator_speed, blaine_fineness, residue_45_micron)
                VALUES (:ts, :mill_type, :feed, :speed, :power, 
                        :dp, :sep_speed, :fineness, :residue)
            """), {
                'ts': timestamp,
                'mill_type': random.choice(['VRM', 'Ball Mill']),
                'feed': feed_rate,
                'speed': 15 + random.uniform(-0.5, 0.5),
                'power': power,
                'dp': 70 + random.uniform(-5, 5),
                'sep_speed': 75 + random.uniform(-5, 5),
                'fineness': 3200 + random.uniform(-100, 100),
                'residue': 12 + random.uniform(-2, 2)
            })
        
        await session.commit()
        logger.info(f"✓ Generated {hours} grinding operations records")


async def generate_quality_data(samples=20):
    """Generate sample quality metrics data"""
    async with AsyncSessionLocal() as session:
        logger.info(f"Generating {samples} quality test samples...")
        
        for i in range(samples):
            timestamp = datetime.now() - timedelta(days=random.randint(0, 7))
            
            # Generate realistic cement strength values
            strength_28d = 45 + random.uniform(-3, 3)
            
            await session.execute(text("""
                INSERT INTO quality_metrics 
                (timestamp, sample_id, compressive_strength_3d, compressive_strength_7d,
                 compressive_strength_28d, free_lime, so3_content, loss_on_ignition,
                 chloride_content, vision_inspection_score, defect_detected)
                VALUES (:ts, :sample_id, :str_3d, :str_7d, :str_28d, 
                        :free_lime, :so3, :loi, :cl, :vision_score, :defect)
            """), {
                'ts': timestamp,
                'sample_id': f'SAMPLE-{i+1:04d}',
                'str_3d': strength_28d * 0.6 + random.uniform(-1, 1),
                'str_7d': strength_28d * 0.8 + random.uniform(-1, 1),
                'str_28d': strength_28d,
                'free_lime': 1.2 + random.uniform(-0.3, 0.3),
                'so3': 2.8 + random.uniform(-0.2, 0.2),
                'loi': 2.5 + random.uniform(-0.3, 0.3),
                'cl': 0.02 + random.uniform(-0.005, 0.005),
                'vision_score': 85 + random.uniform(-10, 10),
                'defect': random.random() < 0.05  # 5% defect rate
            })
        
        await session.commit()
        logger.info(f"✓ Generated {samples} quality test samples")


async def generate_raw_material_data(hours=24):
    """Generate sample raw material feed data"""
    async with AsyncSessionLocal() as session:
        logger.info(f"Generating {hours} hours of raw material data...")
        
        for i in range(hours):
            timestamp = datetime.now() - timedelta(hours=hours-i)
            
            # Realistic raw material composition
            cao = 65 + random.uniform(-2, 2)
            sio2 = 22 + random.uniform(-1, 1)
            al2o3 = 5 + random.uniform(-0.5, 0.5)
            fe2o3 = 3 + random.uniform(-0.3, 0.3)
            
            # Calculate LSF
            lsf = cao / (2.8 * sio2 + 1.2 * al2o3 + 0.65 * fe2o3)
            
            await session.execute(text("""
                INSERT INTO raw_material_feed 
                (timestamp, limestone_rate, clay_rate, iron_ore_rate, gypsum_rate,
                 cao_pct, sio2_pct, al2o3_pct, fe2o3_pct, lsf, sm, am)
                VALUES (:ts, :limestone, :clay, :iron, :gypsum,
                        :cao, :sio2, :al2o3, :fe2o3, :lsf, :sm, :am)
            """), {
                'ts': timestamp,
                'limestone': 80 + random.uniform(-5, 5),
                'clay': 15 + random.uniform(-2, 2),
                'iron': 3 + random.uniform(-0.5, 0.5),
                'gypsum': 2 + random.uniform(-0.3, 0.3),
                'cao': cao,
                'sio2': sio2,
                'al2o3': al2o3,
                'fe2o3': fe2o3,
                'lsf': lsf,
                'sm': sio2 / (al2o3 + fe2o3),
                'am': al2o3 / fe2o3
            })
        
        await session.commit()
        logger.info(f"✓ Generated {hours} raw material feed records")


async def generate_recommendations():
    """Generate sample AI recommendations for JK Cement operations"""
    async with AsyncSessionLocal() as session:
        logger.info("Generating AI recommendations for JK Cement...")
        
        recommendations = [
            {
                'module': 'kiln',
                'type': 'energy_optimization',
                'description': 'Reduce burning zone temperature by 8°C to 1452°C to optimize coal consumption while maintaining JK Super Cement clinker quality standards',
                'priority': 'high',
                'savings': 18000.0,  # ₹/day
                'confidence': 0.92
            },
            {
                'module': 'grinding',
                'type': 'efficiency',
                'description': 'Adjust separator speed to 79 RPM and optimize mill loading for optimal fineness with target <30 kWh/ton specific energy',
                'priority': 'medium',
                'savings': 12000.0,  # ₹/day
                'confidence': 0.87
            },
            {
                'module': 'fuel',
                'type': 'alternative_fuel',
                'description': 'Increase TSR from 28% to 35% - current RDF and biomass quality supports higher substitution. Aligns with JK Cement sustainability goals',
                'priority': 'high',
                'savings': 22000.0,  # ₹/day
                'confidence': 0.95
            },
            {
                'module': 'quality',
                'type': 'process_control',
                'description': 'Raw mix LSF at 91.2, trending low - increase limestone feed by 3.5 tph to maintain target 94 for optimal clinker quality per IS standards',
                'priority': 'medium',
                'savings': 8000.0,  # ₹/day
                'confidence': 0.89
            },
            {
                'module': 'maintenance',
                'type': 'predictive',
                'description': 'Mill-2 bearing temperature at 82°C and trending high - schedule inspection within 48 hours to prevent unplanned shutdown',
                'priority': 'high',
                'savings': 40000.0,  # ₹ - prevented breakdown cost
                'confidence': 0.91
            },
            {
                'module': 'energy',
                'type': 'power_optimization',
                'description': 'Specific power at 118 kWh/ton - optimize mill ventilation and shift high-power operations to off-peak hours (10 PM - 6 AM)',
                'priority': 'medium',
                'savings': 9500.0,  # ₹/day
                'confidence': 0.88
            },
            {
                'module': 'operational',
                'type': 'production',
                'description': 'Kiln feed at 102 tph - capacity analysis shows potential to increase by 3-4 tph for additional production revenue',
                'priority': 'medium',
                'savings': 35000.0,  # ₹/day additional revenue
                'confidence': 0.86
            }
        ]
        
        for rec in recommendations:
            await session.execute(text("""
                INSERT INTO ai_recommendations 
                (timestamp, module, recommendation_type, description, 
                 priority, estimated_savings, confidence_score, status)
                VALUES (NOW(), :module, :type, :description, 
                        :priority, :savings, :confidence, 'pending')
            """), rec)
        
        await session.commit()
        logger.info(f"✓ Generated {len(recommendations)} AI recommendations for JK Cement")


async def main():
    """Main function to generate all sample data for JK Cement"""
    logger.info("Starting JK Cement sample data generation...")
    logger.info("=" * 60)
    
    try:
        # Generate data for different time periods
        await generate_raw_material_data(hours=48)
        await generate_kiln_data(hours=48)
        await generate_grinding_data(hours=48)
        await generate_quality_data(samples=30)
        await generate_recommendations()
        
        logger.info("=" * 60)
        logger.info("✓ JK Cement sample data generation completed successfully!")
        logger.info("")
        logger.info("Generated data includes:")
        logger.info("  • Raw material feed (Indian specifications)")
        logger.info("  • Kiln operations (760-780 kcal/kg target)")
        logger.info("  • Grinding operations (<30 kWh/ton)")
        logger.info("  • Quality metrics (IS 269, IS 12269)")
        logger.info("  • AI recommendations (savings in INR)")
        logger.info("")
        logger.info("You can now:")
        logger.info("  1. Start the backend: python main.py")
        logger.info("  2. Start the frontend: npm run dev")
        logger.info("  3. Navigate to AI Insights & Chat")
        logger.info("  4. Try queries like: 'What's the current kiln efficiency?'")
        
    except Exception as e:
        logger.error(f"✗ Error generating sample data: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
