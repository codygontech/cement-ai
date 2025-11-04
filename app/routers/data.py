"""
Data API Router - Complete endpoints for all data tables
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from sqlalchemy import text
from app.db import session as db_session  # Import module, not the variable
from app.core.logging_config import logger
from datetime import datetime

router = APIRouter()


@router.get("/kiln-operations")
async def get_kiln_operations(limit: int = Query(50, ge=1, le=1000)):
    """Get kiln operations data"""
    try:
        if not db_session.AsyncSessionLocal:  # Access the variable from the module
            logger.warning("Database not configured, returning empty data")
            return []
            
        async with db_session.AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM kiln_operations
                    ORDER BY timestamp DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching kiln operations: {e}")
        # Return empty array instead of 500 error to keep frontend working
        return []


@router.get("/alternative-fuels")
async def get_alternative_fuels(limit: int = Query(50, ge=1, le=1000)):
    """Get alternative fuels data"""
    try:
        if not db_session.AsyncSessionLocal:
            logger.warning("Database not configured, returning empty data")
            return []
            
        async with db_session.AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM alternative_fuels
                    ORDER BY timestamp DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching alternative fuels: {e}")
        return []


@router.get("/optimization-results")
async def get_optimization_results(
    limit: int = Query(50, ge=1, le=1000),
    type: Optional[str] = None
):
    """Get optimization results data"""
    try:
        if not db_session.AsyncSessionLocal:
            logger.warning("Database not configured, returning empty data")
            return []
            
        async with db_session.AsyncSessionLocal() as session:
            if type:
                result = await session.execute(
                    text("""
                        SELECT * FROM optimization_results
                        WHERE optimization_type ILIKE :type
                        ORDER BY timestamp DESC
                        LIMIT :limit
                    """),
                    {"limit": limit, "type": f"%{type}%"}
                )
            else:
                result = await session.execute(
                    text("""
                        SELECT * FROM optimization_results
                        ORDER BY timestamp DESC
                        LIMIT :limit
                    """),
                    {"limit": limit}
                )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching optimization results: {e}")
        return []


@router.get("/utilities-monitoring")
async def get_utilities_monitoring(limit: int = Query(50, ge=1, le=1000)):
    """Get utilities monitoring data"""
    try:
        if not db_session.AsyncSessionLocal:
            logger.warning("Database not configured, returning empty data")
            return []
            
        async with db_session.AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM utilities_monitoring
                    ORDER BY timestamp DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching utilities monitoring: {e}")
        return []


@router.get("/raw-material-feed")
async def get_raw_material_feed(limit: int = Query(50, ge=1, le=1000)):
    """Get raw material feed data"""
    try:
        if not db_session.AsyncSessionLocal:
            logger.warning("Database not configured, returning empty data")
            return []
            
        async with db_session.AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM raw_material_feed
                    ORDER BY timestamp DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching raw material feed: {e}")
        return []


@router.get("/grinding-operations")
async def get_grinding_operations(limit: int = Query(50, ge=1, le=1000)):
    """Get grinding operations data"""
    try:
        if not db_session.AsyncSessionLocal:
            logger.warning("Database not configured, returning empty data")
            return []
            
        async with db_session.AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM grinding_operations
                    ORDER BY timestamp DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching grinding operations: {e}")
        return []


@router.get("/quality-control")
async def get_quality_control(limit: int = Query(50, ge=1, le=1000)):
    """Get quality control data"""
    try:
        if not db_session.AsyncSessionLocal:
            logger.warning("Database not configured, returning empty data")
            return []
            
        async with db_session.AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM quality_control
                    ORDER BY timestamp DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching quality control: {e}")
        return []


@router.get("/ai-recommendations")
async def get_ai_recommendations(status: Optional[str] = None):
    """Get AI recommendations"""
    try:
        if not db_session.AsyncSessionLocal:
            logger.warning("Database not configured, returning empty data")
            return []
            
        async with db_session.AsyncSessionLocal() as session:
            if status:
                result = await session.execute(
                    text("""
                        SELECT * FROM ai_recommendations
                        WHERE status = :status
                        ORDER BY timestamp DESC
                    """),
                    {"status": status}
                )
            else:
                result = await session.execute(
                    text("""
                        SELECT * FROM ai_recommendations
                        ORDER BY timestamp DESC
                        LIMIT 100
                    """)
                )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching AI recommendations: {e}")
        return []

