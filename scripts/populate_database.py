"""
Populate database with sample data for JK Cement India operations
Matches the actual Cloud SQL database schema with India-specific parameters
"""

import asyncio
from datetime import datetime, timedelta
import random
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import AsyncSessionLocal
from sqlalchemy import text


async def populate_kiln_operations(hours=48):
    """Generate kiln operations data for JK Cement plant"""
    async with AsyncSessionLocal() as session:
        print(f"📊 Generating {hours} hours of kiln operations data...")
        
        for i in range(hours):
            timestamp = datetime.now() - timedelta(hours=hours-i)
            
            # JK Cement typical parameters (optimized for Indian conditions)
            feed_rate = 110 + random.uniform(-8, 8)  # tph
            coal_rate = 11 + random.uniform(-1.2, 1.2)  # tph
            alt_fuel_rate = 3.5 + random.uniform(-0.8, 1.2)  # tph - JK Cement's AFR initiative
            temp = 1460 + random.uniform(-25, 25)  # °C - typical for JK plants
            
            await session.execute(text("""
                INSERT INTO kiln_operations 
                (timestamp, feed_rate, kiln_speed, burning_zone_temp, 
                 coal_feed_rate, alternative_fuel_rate, o2_pct, 
                 co_ppm, nox_ppm, clinker_production, free_lime, thermal_consumption)
                VALUES (:ts, :feed, :speed, :temp, :coal, :alt_fuel, 
                        :o2, :co, :nox, :clinker, :free_lime, :thermal)
            """), {
                'ts': timestamp,
                'feed': feed_rate,
                'speed': 3.6 + random.uniform(-0.25, 0.25),  # RPM
                'temp': temp,
                'coal': coal_rate,
                'alt_fuel': alt_fuel_rate,
                'o2': 3.2 + random.uniform(-0.6, 0.6),  # %
                'co': int(45 + random.uniform(-12, 12)),  # ppm - compliant with Indian norms
                'nox': int(750 + random.uniform(-80, 80)),  # ppm - within CPCB limits
                'clinker': feed_rate * 0.92 + random.uniform(-2.5, 2.5),  # tph
                'free_lime': 1.1 + random.uniform(-0.35, 0.35),  # % - JK Cement quality target
                'thermal': 765 + random.uniform(-25, 25)  # kcal/kg - JK Cement efficiency target
            })
        
        await session.commit()
        print(f"✅ Generated {hours} kiln operations records")


async def populate_alternative_fuels(hours=48):
    """Generate alternative fuels data for JK Cement's AFR program"""
    async with AsyncSessionLocal() as session:
        print(f"♻️  Generating {hours} hours of alternative fuels data...")
        
        # JK Cement's AFR mix - aligned with their sustainability initiatives
        fuel_types = ['Biomass', 'RDF', 'Plastic Waste', 'Industrial Waste', 'Pet Coke']
        
        for i in range(hours):
            timestamp = datetime.now() - timedelta(hours=hours-i)
            fuel_type = random.choice(fuel_types)
            quantity = random.uniform(1.5, 6)  # tph
            
            # JK Cement specific fuel properties (Indian market)
            if fuel_type == 'Biomass':
                calorific = 3600 + random.uniform(-250, 250)  # kcal/kg
                cost = 1800 + random.uniform(-200, 200)  # ₹/ton
                co2_factor = 0.02
            elif fuel_type == 'RDF':
                calorific = 4300 + random.uniform(-350, 350)  # kcal/kg
                cost = 1500 + random.uniform(-200, 200)  # ₹/ton - cheaper than coal
                co2_factor = 0.68
            elif fuel_type == 'Industrial Waste':
                calorific = 3900 + random.uniform(-300, 300)  # kcal/kg
                cost = 1200 + random.uniform(-150, 150)  # ₹/ton - very cost effective
                co2_factor = 0.55
            else:
                calorific = 4100 + random.uniform(-300, 300)  # kcal/kg
                cost = 1600 + random.uniform(-200, 200)  # ₹/ton
                co2_factor = 0.5
            
            # Compare with coal cost (~5500-6000 ₹/ton in India)
            coal_cost = 5800
            savings_per_ton = coal_cost - cost
            
            await session.execute(text("""
                INSERT INTO alternative_fuels 
                (timestamp, fuel_type, quantity, calorific_value, 
                 cost_per_ton, co2_emission_factor, tsr, savings_amount)
                VALUES (:ts, :fuel_type, :qty, :calorific, 
                        :cost, :co2, :tsr, :savings)
            """), {
                'ts': timestamp,
                'fuel_type': fuel_type,
                'qty': quantity,
                'calorific': calorific,
                'cost': cost,
                'co2': co2_factor,
                'tsr': 28 + random.uniform(-4, 8),  # % - JK Cement targeting >30%
                'savings': quantity * savings_per_ton  # Daily savings in ₹
            })
        
        await session.commit()
        print(f"✅ Generated {hours} alternative fuels records")


async def populate_grinding_operations(hours=48):
    """Generate grinding operations data for JK Cement mills"""
    async with AsyncSessionLocal() as session:
        print(f"⚙️  Generating {hours} hours of grinding operations data...")
        
        # JK Cement's mill naming convention
        mills = ['Mill-1', 'Mill-2', 'Mill-3']
        
        for i in range(hours):
            timestamp = datetime.now() - timedelta(hours=hours-i)
            mill_id = random.choice(mills)
            
            # JK Cement typical grinding parameters
            feed_rate = 85 + random.uniform(-6, 6)  # tph
            power = feed_rate * 32 + random.uniform(-60, 60)  # kW - targeting <30 kWh/ton
            
            await session.execute(text("""
                INSERT INTO grinding_operations 
                (timestamp, mill_id, feed_rate, mill_speed, separator_speed,
                 power_consumption, product_fineness, residue_45_micron, temperature)
                VALUES (:ts, :mill_id, :feed, :speed, :sep_speed,
                        :power, :fineness, :residue, :temp)
            """), {
                'ts': timestamp,
                'mill_id': mill_id,
                'feed': feed_rate,
                'speed': 15.5 + random.uniform(-0.6, 0.6),  # RPM
                'sep_speed': 76 + random.uniform(-6, 6),  # RPM
                'power': power,
                'fineness': 330 + random.uniform(-25, 25),  # Blaine cm²/g - JK quality standard
                'residue': 11 + random.uniform(-2.5, 2.5),  # % - IS 269 compliance
                'temp': 92 + random.uniform(-6, 6)  # °C
            })
        
        await session.commit()
        print(f"✅ Generated {hours} grinding operations records")


async def populate_quality_control(samples=30):
    """Generate quality control data for JK Cement products"""
    async with AsyncSessionLocal() as session:
        print(f"🔬 Generating {samples} quality control samples...")
        
        # JK Cement product types
        sample_types = ['clinker', 'cement_opc53', 'cement_ppc', 'raw_meal']
        
        for i in range(samples):
            timestamp = datetime.now() - timedelta(hours=random.randint(1, 48))
            sample_type = random.choice(sample_types)
            
            # JK Cement quality standards (IS 269, IS 12269, IS 1489)
            if sample_type == 'cement_opc53':
                # OPC 53 Grade - JK Super Cement specifications
                str_3d = 27 + random.uniform(-2.5, 2.5)  # MPa - min 27
                str_7d = 37 + random.uniform(-3, 3)  # MPa - min 37
                str_28d = 54 + random.uniform(-3, 3)  # MPa - min 53
                fineness = 330 + random.uniform(-20, 20)  # cm²/g - typically 320-360
            elif sample_type == 'cement_ppc':
                # PPC - JK Lakshmi specifications
                str_3d = 16 + random.uniform(-2, 2)  # MPa - min 16
                str_7d = 22 + random.uniform(-2.5, 2.5)  # MPa - min 22
                str_28d = 33 + random.uniform(-2.5, 2.5)  # MPa - min 33
                fineness = 320 + random.uniform(-18, 18)  # cm²/g
            else:
                str_3d = None
                str_7d = None
                str_28d = None
                fineness = None
            
            # Determine status based on IS standards
            if sample_type in ['cement_opc53', 'cement_ppc'] and str_28d:
                if sample_type == 'cement_opc53':
                    if str_28d >= 53:
                        status = 'compliant'
                    elif str_28d >= 50:
                        status = 'warning'
                    else:
                        status = 'non-compliant'
                else:  # PPC
                    if str_28d >= 33:
                        status = 'compliant'
                    elif str_28d >= 31:
                        status = 'warning'
                    else:
                        status = 'non-compliant'
            else:
                status = random.choice(['compliant', 'compliant', 'compliant', 'warning'])
            
            await session.execute(text("""
                INSERT INTO quality_control 
                (timestamp, sample_type, compressive_strength_3d, compressive_strength_7d,
                 compressive_strength_28d, setting_time_initial, setting_time_final,
                 fineness, so3, loss_on_ignition, status)
                VALUES (:ts, :sample_type, :str_3d, :str_7d, :str_28d,
                        :set_initial, :set_final, :fineness, :so3, :loi, :status)
            """), {
                'ts': timestamp,
                'sample_type': sample_type,
                'str_3d': str_3d,
                'str_7d': str_7d,
                'str_28d': str_28d,
                'set_initial': 135 + random.randint(-25, 25) if 'cement' in sample_type else None,  # min - IS standard
                'set_final': 280 + random.randint(-35, 35) if 'cement' in sample_type else None,  # min - IS standard
                'fineness': fineness,
                'so3': 2.6 + random.uniform(-0.25, 0.25),  # % - IS limit <3%
                'loi': 2.3 + random.uniform(-0.35, 0.35),  # % - IS limit varies by type
                'status': status
            })
        
        await session.commit()
        print(f"✅ Generated {samples} quality control samples")


async def populate_raw_material_feed(hours=48):
    """Generate raw material feed data for JK Cement plants"""
    async with AsyncSessionLocal() as session:
        print(f"🪨 Generating {hours} hours of raw material feed data...")
        
        for i in range(hours):
            timestamp = datetime.now() - timedelta(hours=hours-i)
            
            # JK Cement typical raw mix proportions (India-specific)
            limestone = 82 + random.uniform(-6, 6)  # tph - primary component
            clay = 14 + random.uniform(-2.5, 2.5)  # tph
            iron_ore = 2.8 + random.uniform(-0.6, 0.6)  # tph
            gypsum = 1.8 + random.uniform(-0.4, 0.4)  # tph
            
            total_feed = limestone + clay + iron_ore + gypsum
            
            # Calculate LSF, SM, AM - JK Cement quality targets
            lsf = 94 + random.uniform(-3.5, 3.5)  # Target: 92-96
            sm = 2.4 + random.uniform(-0.25, 0.25)  # Silica Modulus: 2.2-2.6
            am = 1.5 + random.uniform(-0.25, 0.25)  # Alumina Modulus: 1.3-1.7
            
            await session.execute(text("""
                INSERT INTO raw_material_feed 
                (timestamp, limestone_qty, clay_qty, iron_ore_qty, gypsum_qty,
                 total_feed_rate, moisture_content, lsf, sm, am)
                VALUES (:ts, :limestone, :clay, :iron, :gypsum,
                        :total, :moisture, :lsf, :sm, :am)
            """), {
                'ts': timestamp,
                'limestone': limestone,
                'clay': clay,
                'iron': iron_ore,
                'gypsum': gypsum,
                'total': total_feed,
                'moisture': 7.5 + random.uniform(-1.2, 1.2),  # % - Indian monsoon conditions
                'lsf': lsf,
                'sm': sm,
                'am': am
            })
        
        await session.commit()
        print(f"✅ Generated {hours} raw material feed records")


async def populate_utilities_monitoring(hours=48):
    """Generate utilities monitoring data for JK Cement plants"""
    async with AsyncSessionLocal() as session:
        print(f"⚡ Generating {hours} hours of utilities monitoring data...")
        
        for i in range(hours):
            timestamp = datetime.now() - timedelta(hours=hours-i)
            
            # JK Cement typical power consumption (Indian grid conditions)
            power = 12500 + random.uniform(-600, 600)  # kW
            production = 108 + random.uniform(-6, 6)  # tph
            specific_power = power / production
            
            # Indian power costs (varies by state and time)
            power_cost_per_kwh = 7.2 + random.uniform(-0.5, 0.5)  # ₹/kWh - typical industrial rate
            
            await session.execute(text("""
                INSERT INTO utilities_monitoring 
                (timestamp, power_consumption, specific_power, water_consumption,
                 compressed_air_pressure, thermal_energy, cost_per_ton)
                VALUES (:ts, :power, :specific, :water, :air, :thermal, :cost)
            """), {
                'ts': timestamp,
                'power': power,
                'specific': specific_power,
                'water': 145 + random.uniform(-12, 12),  # m³/hr - water optimization focus
                'air': 6.8 + random.uniform(-0.4, 0.4),  # bar
                'thermal': 2600 + random.uniform(-120, 120),  # kcal/hr
                'cost': (specific_power * power_cost_per_kwh)  # ₹/ton electricity cost
            })
        
        await session.commit()
        print(f"✅ Generated {hours} utilities monitoring records")


async def populate_optimization_results(count=20):
    """Generate optimization results"""
    async with AsyncSessionLocal() as session:
        print(f"🎯 Generating {count} optimization results...")
        
        optimization_types = ['fuel', 'raw_mix', 'kiln_speed', 'grinding']
        parameters = {
            'fuel': ['Coal Feed Rate', 'Alt Fuel Rate', 'TSR'],
            'raw_mix': ['LSF', 'SM', 'AM', 'Feed Rate'],
            'kiln_speed': ['RPM', 'Burning Zone Temp'],
            'grinding': ['Mill Speed', 'Separator Speed', 'Feed Rate']
        }
        
        for i in range(count):
            timestamp = datetime.now() - timedelta(days=random.randint(0, 7))
            opt_type = random.choice(optimization_types)
            param = random.choice(parameters[opt_type])
            
            current = 100 + random.uniform(-20, 20)
            recommended = current + random.uniform(-5, 10)
            
            status_choices = ['pending', 'pending', 'implemented', 'rejected']
            status = random.choice(status_choices)
            
            await session.execute(text("""
                INSERT INTO optimization_results 
                (timestamp, optimization_type, parameter_name, current_value,
                 recommended_value, expected_savings, confidence_score,
                 implementation_status, actual_savings)
                VALUES (:ts, :opt_type, :param, :current, :recommended,
                        :expected, :confidence, :status, :actual)
            """), {
                'ts': timestamp,
                'opt_type': opt_type,
                'param': param,
                'current': current,
                'recommended': recommended,
                'expected': random.uniform(5000, 25000),
                'confidence': random.uniform(0.75, 0.98),
                'status': status,
                'actual': random.uniform(4000, 20000) if status == 'implemented' else None
            })
        
        await session.commit()
        print(f"✅ Generated {count} optimization results")


async def populate_ai_recommendations(count=15):
    """Generate AI recommendations tailored for JK Cement India operations"""
    async with AsyncSessionLocal() as session:
        print(f"🤖 Generating {count} AI recommendations...")
        
        recommendations = [
            ('operational', 'Optimize Kiln Thermal Efficiency', 
             'Reduce burning zone temperature by 8°C to 1452°C to optimize fuel consumption while maintaining clinker quality per JK standards',
             'high', 'Reduce coal cost by ₹18,000/day (₹6.5 lakh/month)'),
            ('operational', 'Increase Alternative Fuel Rate',
             'Increase TSR from 28% to 35% - current RDF and biomass quality supports higher substitution. JK Cement sustainability target alignment.',
             'high', 'Save ₹22,000/day on fuel costs (₹8 lakh/month)'),
            ('operational', 'Optimize Grinding Mill Energy',
             'Adjust separator speed to 79 RPM and optimize mill loading to achieve <30 kWh/ton specific energy',
             'medium', 'Reduce power consumption by ₹12,000/day'),
            ('quality', 'Raw Mix LSF Control',
             'Raw mix LSF trending at 91.2 - increase limestone feed by 3.5 tph to maintain target 94 for optimal clinker quality',
             'medium', 'Maintain JK Super Cement quality consistency'),
            ('maintenance', 'Mill Bearing Preventive Action',
             'Mill-2 bearing temperature at 82°C and trending high - schedule inspection within 48 hours to prevent breakdown',
             'high', 'Prevent unplanned shutdown (₹40,000 potential savings)'),
            ('energy', 'Power Demand Management',
             'Specific power at 118 kWh/ton, 4% above target - optimize mill ventilation and loading during off-peak tariff hours',
             'medium', 'Save ₹9,500/day on electricity (₹3.4 lakh/month)'),
            ('quality', 'Cement Fineness Consistency',
             'OPC 53 fineness showing ±15 cm²/g variation - adjust separator control for better consistency per IS 12269',
             'low', 'Improve JK Super Cement product quality consistency'),
            ('operational', 'Kiln Feed Rate Optimization',
             'Current kiln feed at 102 tph - capacity analysis shows potential to increase by 3-4 tph based on system capacity',
             'medium', 'Increase production by 72-96 tpd (₹2.5-3 lakh/day revenue)'),
            ('maintenance', 'Cooler Efficiency Maintenance',
             'Clinker cooler thermal efficiency declining to 68% - plan grate cleaning during next scheduled maintenance',
             'low', 'Maintain thermal efficiency and fuel consumption'),
            ('energy', 'Compressed Air System Optimization',
             'Compressed air pressure at 7.2 bar, higher than required - reduce to 6.5 bar to save compressor power',
             'low', 'Save ₹3,200/day on power (₹1.15 lakh/month)'),
            ('operational', 'Raw Material Moisture Control',
             'Raw meal moisture at 8.5% - optimize drying to 7% for better pyro-processing efficiency',
             'medium', 'Reduce thermal energy by ₹7,000/day'),
            ('quality', 'SO3 Content Monitoring',
             'SO3 trending at 2.75% - optimize gypsum addition to maintain 2.5% for better cement performance',
             'low', 'Ensure IS 269 compliance and product quality'),
            ('operational', 'AFR Waste Heat Recovery',
             'Install WHR system for kiln exit gases - feasibility for 6-8 MW power generation',
             'high', 'Potential savings ₹15-20 lakh/month after installation'),
            ('maintenance', 'Separator Efficiency Check',
             'Separator efficiency at 72% - check vanes and adjust air flow for optimal 75-78% efficiency',
             'medium', 'Improve grinding efficiency and product quality'),
            ('energy', 'Peak Load Management',
             'Shift high-power operations to off-peak hours (10 PM - 6 AM) to benefit from lower tariff rates',
             'medium', 'Save ₹25,000-30,000/month on power bills'),
        ]
        
        for i in range(min(count, len(recommendations))):
            rec = recommendations[i]
            timestamp = datetime.now() - timedelta(hours=random.randint(1, 168))
            
            status_choices = ['new', 'new', 'reviewed', 'implemented', 'closed']
            status = random.choice(status_choices)
            
            await session.execute(text("""
                INSERT INTO ai_recommendations 
                (timestamp, category, title, description, priority,
                 expected_impact, status, implementation_date, feedback)
                VALUES (:ts, :category, :title, :description, :priority,
                        :impact, :status, :impl_date, :feedback)
            """), {
                'ts': timestamp,
                'category': rec[0],
                'title': rec[1],
                'description': rec[2],
                'priority': rec[3],
                'impact': rec[4],
                'status': status,
                'impl_date': datetime.now() - timedelta(days=random.randint(1, 5)) if status == 'implemented' else None,
                'feedback': 'Successfully implemented - positive results observed' if status == 'implemented' else None
            })
        
        await session.commit()
        print(f"✅ Generated {count} AI recommendations")


async def main():
    """Populate all tables with JK Cement India specific sample data"""
    print("\n" + "="*60)
    print("  JK Cement AI Optimization - Database Population")
    print("  Generating India-specific operational data")
    print("="*60 + "\n")
    
    try:
        await populate_raw_material_feed(hours=48)
        await populate_kiln_operations(hours=48)
        await populate_alternative_fuels(hours=48)
        await populate_grinding_operations(hours=48)
        await populate_utilities_monitoring(hours=48)
        await populate_quality_control(samples=30)
        await populate_optimization_results(count=20)
        await populate_ai_recommendations(count=15)
        
        print("\n" + "="*60)
        print("  ✅ JK Cement database population completed successfully!")
        print("="*60 + "\n")
        print("Data generated for:")
        print("  • Raw material feed with Indian specifications")
        print("  • Kiln operations (targeting 760-780 kcal/kg)")
        print("  • Alternative fuels (RDF, Biomass, Industrial waste)")
        print("  • Grinding operations (<30 kWh/ton target)")
        print("  • Quality control (IS 269, IS 12269, IS 1489)")
        print("  • AI recommendations with INR cost savings")
        print("\nNext steps:")
        print("  1. Backend running on http://localhost:8000")
        print("  2. Frontend running on http://localhost:3000")
        print("  3. All costs displayed in Indian Rupees (₹)")
        print()
        
    except Exception as e:
        print(f"\n❌ Error populating database: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
