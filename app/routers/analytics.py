"""
Analytics API Router
Advanced analytics and insights
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from app.core.logging_config import logger
from app.db import session as db_session
from sqlalchemy import text

router = APIRouter()


class OptimizationOpportunity(BaseModel):
    """Optimization opportunity model"""
    category: str
    description: str
    estimated_savings: float
    implementation_difficulty: str
    priority: str


@router.get("/opportunities")
async def get_optimization_opportunities():
    """
    Identify optimization opportunities across the plant
    """
    try:
        opportunities = []
        
        async with db_session.AsyncSessionLocal() as session:
            # Check kiln efficiency
            kiln_result = await session.execute(
                text("""
                    SELECT AVG(alternative_fuel_rate::float / NULLIF((coal_feed_rate + alternative_fuel_rate), 0) * 100) as alt_fuel_pct
                    FROM kiln_operations
                    WHERE timestamp >= NOW() - INTERVAL '24 hours'
                """)
            )
            alt_fuel_pct = kiln_result.scalar()
            
            if alt_fuel_pct and alt_fuel_pct < 30:
                opportunities.append({
                    "category": "Fuel Optimization",
                    "description": f"Increase alternative fuel rate from {alt_fuel_pct:.1f}% to 35% target",
                    "estimated_savings": 150000.0,
                    "implementation_difficulty": "Medium",
                    "priority": "High"
                })
            
            # Check grinding energy
            grinding_result = await session.execute(
                text("""
                    SELECT AVG(power_consumption / NULLIF(feed_rate, 0)) as specific_energy
                    FROM grinding_operations
                    WHERE timestamp >= NOW() - INTERVAL '24 hours'
                """)
            )
            specific_energy = grinding_result.scalar()
            
            if specific_energy and specific_energy > 35:
                opportunities.append({
                    "category": "Energy Optimization",
                    "description": f"Reduce grinding specific energy from {specific_energy:.1f} to <35 kWh/ton",
                    "estimated_savings": 80000.0,
                    "implementation_difficulty": "Medium",
                    "priority": "High"
                })
            
            # Check quality defect rate
            quality_result = await session.execute(
                text("""
                    SELECT COUNT(CASE WHEN defect_detected THEN 1 END)::float / NULLIF(COUNT(*), 0)::float * 100 as defect_rate
                    FROM quality_metrics
                    WHERE timestamp >= NOW() - INTERVAL '7 days'
                """)
            )
            defect_rate = quality_result.scalar()
            
            if defect_rate and defect_rate > 2:
                opportunities.append({
                    "category": "Quality Control",
                    "description": f"Reduce defect rate from {defect_rate:.1f}% to <1%",
                    "estimated_savings": 50000.0,
                    "implementation_difficulty": "Low",
                    "priority": "Medium"
                })
        
        # Add general opportunities
        opportunities.extend([
            {
                "category": "Predictive Maintenance",
                "description": "Implement AI-powered predictive maintenance for kiln and mills",
                "estimated_savings": 200000.0,
                "implementation_difficulty": "High",
                "priority": "High"
            },
            {
                "category": "Process Integration",
                "description": "Optimize cross-process parameters for holistic efficiency",
                "estimated_savings": 120000.0,
                "implementation_difficulty": "Medium",
                "priority": "Medium"
            }
        ])
        
        return {
            "opportunities": opportunities,
            "total_estimated_savings": sum(opp["estimated_savings"] for opp in opportunities),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error calculating opportunities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kpis")
async def get_kpis():
    """
    Get key performance indicators
    """
    try:
        async with db_session.AsyncSessionLocal() as session:
            # Overall plant efficiency
            result = await session.execute(
                text("""
                    WITH kiln_metrics AS (
                        SELECT AVG(clinker_production) as production
                        FROM kiln_operations
                        WHERE timestamp >= NOW() - INTERVAL '24 hours'
                    ),
                    energy_metrics AS (
                        SELECT AVG(power_consumption / NULLIF(feed_rate, 0)) as specific_energy
                        FROM grinding_operations
                        WHERE timestamp >= NOW() - INTERVAL '24 hours'
                    ),
                    quality_metrics AS (
                        SELECT 
                            AVG(compressive_strength_28d) as avg_strength,
                            COUNT(CASE WHEN defect_detected THEN 1 END)::float / NULLIF(COUNT(*), 0)::float * 100 as defect_rate
                        FROM quality_metrics
                        WHERE timestamp >= NOW() - INTERVAL '24 hours'
                    )
                    SELECT 
                        k.production,
                        e.specific_energy,
                        q.avg_strength,
                        q.defect_rate
                    FROM kiln_metrics k, energy_metrics e, quality_metrics q
                """)
            )
            
            data = result.fetchone()
            
            if data:
                return {
                    "production_efficiency": {
                        "value": round(data[0] / 100 * 100, 2) if data[0] else 0,  # % of target
                        "target": 100.0,
                        "unit": "%"
                    },
                    "energy_efficiency": {
                        "value": round(max(0, 100 - data[1]), 2) if data[1] else 0,
                        "target": 100.0,
                        "unit": "%"
                    },
                    "quality_score": {
                        "value": round(100 - (data[3] if data[3] else 0), 2),
                        "target": 99.0,
                        "unit": "%"
                    },
                    "overall_equipment_effectiveness": {
                        "value": 85.5,
                        "target": 90.0,
                        "unit": "%"
                    },
                    "timestamp": datetime.now().isoformat()
                }
        
        return {"error": "No data available"}
        
    except Exception as e:
        logger.error(f"Error calculating KPIs: {e}")
        raise HTTPException(status_code=500, detail=str(e))
