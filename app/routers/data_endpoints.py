"""
Enhanced Data API Router with all required endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from sqlalchemy import text, select
from app.db.session import AsyncSessionLocal
from app.core.logging_config import logger

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/kiln-operations")
async def get_kiln_operations(limit: int = Query(50, ge=1, le=1000)):
    """Get kiln operations data"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM kiln_operations
                    ORDER BY created_at DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching kiln operations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alternative-fuels")
async def get_alternative_fuels(limit: int = Query(50, ge=1, le=1000)):
    """Get alternative fuels data"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM alternative_fuels
                    ORDER BY created_at DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching alternative fuels: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/optimization-results")
async def get_optimization_results(
    limit: int = Query(50, ge=1, le=1000),
    type: Optional[str] = None
):
    """Get optimization results data"""
    try:
        async with AsyncSessionLocal() as session:
            if type:
                result = await session.execute(
                    text("""
                        SELECT * FROM optimization_results
                        WHERE optimization_type ILIKE :type
                        ORDER BY created_at DESC
                        LIMIT :limit
                    """),
                    {"limit": limit, "type": f"%{type}%"}
                )
            else:
                result = await session.execute(
                    text("""
                        SELECT * FROM optimization_results
                        ORDER BY created_at DESC
                        LIMIT :limit
                    """),
                    {"limit": limit}
                )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching optimization results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/utilities-monitoring")
async def get_utilities_monitoring(limit: int = Query(50, ge=1, le=1000)):
    """Get utilities monitoring data"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM utilities_monitoring
                    ORDER BY created_at DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching utilities monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/raw-material-feed")
async def get_raw_material_feed(limit: int = Query(50, ge=1, le=1000)):
    """Get raw material feed data"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM raw_material_feed
                    ORDER BY created_at DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching raw material feed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/grinding-operations")
async def get_grinding_operations(limit: int = Query(50, ge=1, le=1000)):
    """Get grinding operations data"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM grinding_operations
                    ORDER BY created_at DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching grinding operations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quality-control")
async def get_quality_control(limit: int = Query(50, ge=1, le=1000)):
    """Get quality control data"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT * FROM quality_control
                    ORDER BY created_at DESC
                    LIMIT :limit
                """),
                {"limit": limit}
            )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching quality control: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ai-recommendations")
async def get_ai_recommendations(status: Optional[str] = None):
    """Get AI recommendations"""
    try:
        async with AsyncSessionLocal() as session:
            if status:
                result = await session.execute(
                    text("""
                        SELECT * FROM ai_recommendations
                        WHERE status = :status
                        ORDER BY created_at DESC
                    """),
                    {"status": status}
                )
            else:
                result = await session.execute(
                    text("""
                        SELECT * FROM ai_recommendations
                        ORDER BY created_at DESC
                        LIMIT 100
                    """)
                )
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching AI recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))
