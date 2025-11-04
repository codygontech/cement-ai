"""
Plant Locations API Router for JK Cement
Handles CRUD operations for JK Cement plant locations across India
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import text

from app.db import session as db_session
from app.core.logging_config import logger

router = APIRouter()


class PlantLocationBase(BaseModel):
    """Base plant location model"""
    plant_code: str = Field(..., description="Unique plant code")
    plant_name: str = Field(..., description="Plant name")
    location: str = Field(..., description="Location address")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State name")
    country: str = Field(default="India", description="Country")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    capacity_tpd: Optional[int] = Field(None, description="Capacity in tons per day")
    plant_type: Optional[str] = Field(None, description="Plant type (Integrated, Grinding Unit, etc.)")
    commissioned_year: Optional[int] = Field(None, description="Year commissioned")
    status: str = Field(default="operational", description="Plant status")
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class PlantLocationResponse(PlantLocationBase):
    """Plant location response model"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PlantLocationStats(BaseModel):
    """Plant location statistics"""
    total_plants: int
    operational_plants: int
    total_capacity_tpd: int
    states_covered: int
    plants_by_state: Dict[str, int]
    plants_by_type: Dict[str, int]


@router.get("/locations", response_model=List[PlantLocationResponse])
async def get_all_locations(
    state: Optional[str] = Query(None, description="Filter by state"),
    status: Optional[str] = Query(None, description="Filter by status"),
    plant_type: Optional[str] = Query(None, description="Filter by plant type")
):
    """
    Get all JK Cement plant locations
    
    - **state**: Filter by state (e.g., Rajasthan, Gujarat)
    - **status**: Filter by status (operational, maintenance, planned)
    - **plant_type**: Filter by plant type (Integrated, Grinding Unit, etc.)
    """
    try:
        # Check if database session is available
        if db_session.AsyncSessionLocal is None:
            logger.warning("Database session not available, returning empty list")
            return []
        
        async with db_session.AsyncSessionLocal() as session:
            query = "SELECT * FROM plant_locations WHERE 1=1"
            params = {}
            
            if state:
                query += " AND state = :state"
                params['state'] = state
            
            if status:
                query += " AND status = :status"
                params['status'] = status
            
            if plant_type:
                query += " AND plant_type = :plant_type"
                params['plant_type'] = plant_type
            
            query += " ORDER BY plant_name"
            
            result = await session.execute(text(query), params)
            rows = result.fetchall()
            columns = result.keys()
            
            locations = [dict(zip(columns, row)) for row in rows]
            
            return locations
    
    except Exception as e:
        logger.error(f"Error fetching plant locations: {e}")
        # Return empty list instead of raising HTTPException
        return []


@router.get("/locations/{plant_code}", response_model=PlantLocationResponse)
async def get_location_by_code(plant_code: str):
    """
    Get a specific plant location by plant code
    
    - **plant_code**: Unique plant code (e.g., JK-NIMBAHERA, JK-MANGROL)
    """
    try:
        async with db_session.AsyncSessionLocal() as session:
            query = text("""
                SELECT * FROM plant_locations 
                WHERE plant_code = :plant_code
            """)
            
            result = await session.execute(query, {"plant_code": plant_code})
            row = result.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail=f"Plant with code {plant_code} not found")
            
            columns = result.keys()
            location = dict(zip(columns, row))
            
            return location
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching plant location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locations/nearby/{plant_code}")
async def get_nearby_plants(
    plant_code: str,
    radius_km: float = Query(500, description="Search radius in kilometers", ge=1, le=2000)
):
    """
    Get nearby JK Cement plants within a specified radius
    
    Uses Haversine formula to calculate distance between coordinates
    
    - **plant_code**: Reference plant code
    - **radius_km**: Search radius in kilometers (default: 500km)
    """
    try:
        async with db_session.AsyncSessionLocal() as session:
            # First get the reference plant
            ref_query = text("SELECT * FROM plant_locations WHERE plant_code = :plant_code")
            ref_result = await session.execute(ref_query, {"plant_code": plant_code})
            ref_row = ref_result.fetchone()
            
            if not ref_row:
                raise HTTPException(status_code=404, detail=f"Plant with code {plant_code} not found")
            
            ref_columns = ref_result.keys()
            ref_plant = dict(zip(ref_columns, ref_row))
            ref_lat = ref_plant['latitude']
            ref_lon = ref_plant['longitude']
            
            # Query to find nearby plants using Haversine formula
            query = text("""
                SELECT *,
                    (6371 * acos(
                        cos(radians(:lat)) * cos(radians(latitude)) *
                        cos(radians(longitude) - radians(:lon)) +
                        sin(radians(:lat)) * sin(radians(latitude))
                    )) AS distance_km
                FROM plant_locations
                WHERE plant_code != :plant_code
                HAVING distance_km <= :radius
                ORDER BY distance_km
            """)
            
            result = await session.execute(query, {
                "lat": ref_lat,
                "lon": ref_lon,
                "plant_code": plant_code,
                "radius": radius_km
            })
            
            rows = result.fetchall()
            columns = result.keys()
            
            nearby_plants = [dict(zip(columns, row)) for row in rows]
            
            return {
                "reference_plant": ref_plant,
                "nearby_plants": nearby_plants,
                "search_radius_km": radius_km,
                "count": len(nearby_plants)
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finding nearby plants: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locations/stats/summary", response_model=PlantLocationStats)
async def get_location_stats():
    """
    Get statistical summary of JK Cement plant locations
    
    Returns total plants, capacity, distribution by state and type
    """
    try:
        # Check if database session is available
        if db_session.AsyncSessionLocal is None:
            logger.warning("Database session not available, returning default stats")
            return {
                "total_plants": 0,
                "operational_plants": 0,
                "planned_plants": 0,
                "total_capacity_tpd": 0,
                "states_covered": 0,
                "plant_types": {}
            }
        
        async with db_session.AsyncSessionLocal() as session:
            # Total plants and capacity
            total_query = text("""
                SELECT 
                    COUNT(*) as total_plants,
                    COUNT(CASE WHEN status = 'operational' THEN 1 END) as operational_plants,
                    COALESCE(SUM(capacity_tpd), 0) as total_capacity,
                    COUNT(DISTINCT state) as states_covered
                FROM plant_locations
            """)
            
            total_result = await session.execute(total_query)
            total_row = total_result.fetchone()
            
            # Plants by state
            state_query = text("""
                SELECT state, COUNT(*) as count
                FROM plant_locations
                GROUP BY state
                ORDER BY count DESC
            """)
            
            state_result = await session.execute(state_query)
            state_rows = state_result.fetchall()
            plants_by_state = {row[0]: row[1] for row in state_rows}
            
            # Plants by type
            type_query = text("""
                SELECT plant_type, COUNT(*) as count
                FROM plant_locations
                WHERE plant_type IS NOT NULL
                GROUP BY plant_type
                ORDER BY count DESC
            """)
            
            type_result = await session.execute(type_query)
            type_rows = type_result.fetchall()
            plants_by_type = {row[0]: row[1] for row in type_rows}
            
            return {
                "total_plants": total_row[0],
                "operational_plants": total_row[1],
                "total_capacity_tpd": total_row[2],
                "states_covered": total_row[3],
                "plants_by_state": plants_by_state,
                "plants_by_type": plants_by_type
            }
    
    except Exception as e:
        logger.error(f"Error fetching location stats: {e}")
        # Return default stats instead of raising HTTPException
        return {
            "total_plants": 0,
            "operational_plants": 0,
            "planned_plants": 0,
            "total_capacity_tpd": 0,
            "states_covered": 0,
            "plant_types": {}
        }


@router.get("/locations/state/{state}")
async def get_locations_by_state(state: str):
    """
    Get all plant locations in a specific state
    
    - **state**: State name (e.g., Rajasthan, Gujarat, Andhra Pradesh)
    """
    try:
        async with db_session.AsyncSessionLocal() as session:
            query = text("""
                SELECT * FROM plant_locations 
                WHERE state = :state
                ORDER BY plant_name
            """)
            
            result = await session.execute(query, {"state": state})
            rows = result.fetchall()
            
            if not rows:
                return {
                    "state": state,
                    "plants": [],
                    "count": 0,
                    "total_capacity_tpd": 0
                }
            
            columns = result.keys()
            locations = [dict(zip(columns, row)) for row in rows]
            
            total_capacity = sum(loc.get('capacity_tpd', 0) or 0 for loc in locations)
            
            return {
                "state": state,
                "plants": locations,
                "count": len(locations),
                "total_capacity_tpd": total_capacity
            }
    
    except Exception as e:
        logger.error(f"Error fetching locations by state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locations/map/markers")
async def get_map_markers():
    """
    Get simplified location data optimized for map markers
    
    Returns essential information for displaying plants on a map
    """
    try:
        async with db_session.AsyncSessionLocal() as session:
            query = text("""
                SELECT 
                    plant_code,
                    plant_name,
                    city,
                    state,
                    latitude,
                    longitude,
                    capacity_tpd,
                    plant_type,
                    status
                FROM plant_locations
                ORDER BY plant_name
            """)
            
            result = await session.execute(query)
            rows = result.fetchall()
            columns = result.keys()
            
            markers = [dict(zip(columns, row)) for row in rows]
            
            return {
                "markers": markers,
                "count": len(markers),
                "center": {
                    "latitude": 23.0225,  # Center of India
                    "longitude": 72.5714
                }
            }
    
    except Exception as e:
        logger.error(f"Error fetching map markers: {e}")
        raise HTTPException(status_code=500, detail=str(e))
