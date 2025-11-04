"""
JK Cement AI Optimization System - Backend API
Main FastAPI application with Google Cloud integration for JK Cement India
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from app.core.config import settings
from app.core.logging_config import logger
from app.core.simple_protection import cleanup_old_data
from app.core.telemetry import track_startup, track_shutdown
from app.db.session import init_db, init_engine, cleanup_connector
from app.routers import data, ai_chat, vision, analytics, locations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    logger.info("Starting JK Cement AI Optimization Backend")
    logger.info(f"Google Cloud Project: {settings.GOOGLE_CLOUD_PROJECT}")
    logger.info(f"Region: {settings.VERTEX_AI_LOCATION} (India)")
    
    # Initialize database engine and tables
    try:
        if settings.DATABASE_URL or settings.JDBC_DB_STRING:
            logger.info(f"Initializing database with USE_CLOUD_SQL_PROXY={settings.USE_CLOUD_SQL_PROXY}")
            if settings.USE_CLOUD_SQL_PROXY:
                logger.info(f"Using DATABASE_URL: {settings.DATABASE_URL[:50]}..." if settings.DATABASE_URL else "DATABASE_URL not set!")
            else:
                logger.info(f"Using JDBC_DB_STRING: {settings.JDBC_DB_STRING}")
                logger.info(f"DATABASE_USER: {settings.DATABASE_USER}")
                logger.info(f"DATABASE_NAME: {settings.DATABASE_NAME}")
            
            # Initialize engine first (this will also init connector if needed)
            await init_engine()
            logger.info("Database engine initialized successfully")
            
            # Then initialize tables
            await init_db()
            logger.info("Database tables initialized successfully")
        else:
            logger.warning("Neither DATABASE_URL nor JDBC_DB_STRING set, skipping database initialization")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}", exc_info=True)
        logger.error("Application will continue but database operations will return empty data")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
    
    # Start background cleanup task for rate limiting
    cleanup_task = asyncio.create_task(cleanup_old_data())
    logger.info("Simple protection cleanup task started")
    
    # Track application startup (anonymous telemetry)
    await track_startup()
    
    yield
    
    # Shutdown
    cleanup_task.cancel()
    
    # Track application shutdown (anonymous telemetry)
    await track_shutdown()
    
    # Cleanup Cloud SQL connector
    try:
        await cleanup_connector()
        logger.info("Cloud SQL Connector cleaned up successfully")
    except Exception as e:
        logger.warning(f"Error cleaning up Cloud SQL Connector: {e}")
    
    logger.info("Shutting down JK Cement AI Optimization Backend")


app = FastAPI(
    title="JK Cement AI Optimization API",
    description="Google Cloud-powered AI system for JK Cement India plant optimization and operational excellence",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(ai_chat.router, prefix="/api/ai", tags=["AI Chat"])
app.include_router(vision.router, prefix="/api/vision", tags=["Vision"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(locations.router, prefix="/api", tags=["Plant Locations"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "JK Cement AI Optimization System",
        "company": "JK Cement India",
        "version": "1.0.0",
        "google_cloud": {
            "project": settings.GOOGLE_CLOUD_PROJECT,
            "region": settings.VERTEX_AI_LOCATION,
            "vertex_ai_model": settings.VERTEX_AI_MODEL,
            "cloud_logging": settings.ENABLE_CLOUD_LOGGING,
        },
        "features": [
            "Real-time plant monitoring",
            "AI-powered optimization recommendations",
            "Alternative fuel optimization",
            "Quality control (IS standards)",
            "Energy efficiency tracking",
            "Predictive maintenance",
            "Multi-plant location tracking"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "jk-cement-ai-backend", "company": "JK Cement India"}


@app.get("/db-check")
async def database_connectivity_check():
    """Check database connectivity"""
    from app.db.session import engine
    from sqlalchemy import text
    
    if not engine:
        return {
            "status": "not_configured",
            "message": "Database URL not configured",
            "connected": False
        }
    
    try:
        # Try to execute a simple query
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()  # Don't await - fetchone() is synchronous
        
        return {
            "status": "success",
            "message": "Database connection successful",
            "connected": True,
            "database": "Cloud SQL PostgreSQL"
        }
    except Exception as e:
        logger.error(f"Database connectivity check failed: {e}")
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}",
            "connected": False
        }
