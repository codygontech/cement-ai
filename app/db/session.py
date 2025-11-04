"""
Database connection and session management
Supports both Cloud SQL proxy connection (DATABASE_URL) and direct JDBC connection (JDBC_DB_STRING)
Based on USE_CLOUD_SQL_PROXY environment variable
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from typing import Optional
import os
from urllib.parse import quote_plus


# Global connector instance - must be created once and reused
_connector = None
_connector_initialized = False


def parse_jdbc_connection_string(jdbc_string: str) -> dict:
    """
    Parse JDBC PostgreSQL connection string to extract connection parameters.
    
    Example JDBC string:
    jdbc:postgresql:///cement_plant?cloudSqlInstance=project:region:instance
    jdbc:postgresql://host:port/database?param=value
    
    Returns dict with: host, port, database, and additional params
    """
    # Remove jdbc:postgresql:// or jdbc:postgresql: prefix
    if jdbc_string.startswith("jdbc:postgresql://"):
        jdbc_string = jdbc_string[18:]
    elif jdbc_string.startswith("jdbc:postgresql:"):
        jdbc_string = jdbc_string[16:]
    
    # Parse the connection string
    params = {
        'host': None,
        'port': 5432,
        'database': None,
        'cloudSqlInstance': None,
        'additional_params': {}
    }
    
    # Split by ? to separate main part from query parameters
    parts = jdbc_string.split('?', 1)
    main_part = parts[0]
    query_part = parts[1] if len(parts) > 1 else None
    
    # Parse main part (host:port/database or ///database)
    if main_part.startswith('///'):
        # Format: ///database
        database_part = main_part[3:]
        # Remove leading slash if present
        params['database'] = database_part.lstrip('/')
    elif main_part.startswith('//'):
        # Format: //host:port/database
        main_part = main_part[2:]
        if '/' in main_part:
            host_port, database = main_part.split('/', 1)
            params['database'] = database
            if ':' in host_port:
                params['host'], port_str = host_port.split(':', 1)
                params['port'] = int(port_str)
            else:
                params['host'] = host_port
        else:
            params['host'] = main_part
    elif main_part.startswith('/'):
        # Format: /database (sometimes used)
        params['database'] = main_part[1:]
    else:
        # Assume it's just the database name
        params['database'] = main_part
    
    # Parse query parameters
    if query_part:
        for param_pair in query_part.split('&'):
            if '=' in param_pair:
                key, value = param_pair.split('=', 1)
                if key == 'cloudSqlInstance':
                    params['cloudSqlInstance'] = value
                else:
                    params['additional_params'][key] = value
    
    return params


async def init_connector():
    """Initialize the Cloud SQL connector once per application lifecycle"""
    global _connector, _connector_initialized
    
    if _connector_initialized:
        return _connector
    
    try:
        from google.cloud.sql.connector import Connector
        import asyncio
        
        # Get the current running event loop
        loop = asyncio.get_running_loop()
        
        # Create connector with the specific event loop
        _connector = Connector(loop=loop)
        _connector_initialized = True
        return _connector
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Cloud SQL Connector: {e}")


async def cleanup_connector():
    """Cleanup the Cloud SQL connector on application shutdown"""
    global _connector, _connector_initialized
    
    if _connector and _connector_initialized:
        try:
            await _connector.close_async()
        except Exception:
            pass
        finally:
            _connector = None
            _connector_initialized = False


def _create_standard_engine(jdbc_params: dict):
    """Create a standard asyncpg engine (non-Cloud SQL Connector)"""
    host = jdbc_params['host'] or 'localhost'
    port = jdbc_params['port']
    database = jdbc_params['database'] or settings.DATABASE_NAME
    user = quote_plus(settings.DATABASE_USER)
    password = quote_plus(settings.DATABASE_PASSWORD)
    
    # Construct the connection URL
    connection_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    
    connect_args = {}
    
    # Add any additional parameters
    if jdbc_params['additional_params']:
        connect_args['server_settings'] = jdbc_params['additional_params']
    
    # If running in Cloud Run, add timeout settings
    if os.getenv("K_SERVICE"):
        if 'server_settings' not in connect_args:
            connect_args['server_settings'] = {}
        connect_args['server_settings']['jit'] = 'off'
        connect_args['connect_timeout'] = 30
        connect_args['command_timeout'] = 30
    
    return create_async_engine(
        connection_url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=3600,
        connect_args=connect_args if connect_args else {},
    )


def _create_cloud_sql_engine(jdbc_params: dict):
    """Create an engine using Cloud SQL Connector"""
    async def getconn():
        """Get a connection using the global connector instance"""
        global _connector
        
        if not _connector:
            raise RuntimeError("Cloud SQL Connector not initialized. Call init_connector() first.")
        
        try:
            conn = await _connector.connect_async(
                jdbc_params['cloudSqlInstance'],
                "asyncpg",
                user=settings.DATABASE_USER,
                password=settings.DATABASE_PASSWORD,
                db=jdbc_params['database'] or settings.DATABASE_NAME,
            )
            return conn
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Cloud SQL: {e}")
    
    return create_async_engine(
        "postgresql+asyncpg://",
        async_creator=getconn,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=3600,
    )


# Engine and session will be created during initialization
engine: Optional[create_async_engine] = None
AsyncSessionLocal = None
_engine_initialized = False

Base = declarative_base()


async def init_engine():
    """Initialize the database engine (must be called from async context)"""
    global engine, AsyncSessionLocal, _engine_initialized
    
    if _engine_initialized:
        return engine
    
    try:
        if settings.USE_CLOUD_SQL_PROXY:
            # Use DATABASE_URL when proxy is enabled
            if not settings.DATABASE_URL:
                raise RuntimeError("DATABASE_URL not set but USE_CLOUD_SQL_PROXY is True")
            
            connect_args = {}
            
            # If running in Cloud Run, add timeout settings
            if os.getenv("K_SERVICE"):
                connect_args = {
                    "server_settings": {"jit": "off"},
                    "connect_timeout": 30,
                    "command_timeout": 30,
                }
            
            engine = create_async_engine(
                settings.DATABASE_URL,
                echo=settings.DEBUG,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
                pool_recycle=3600,
                connect_args=connect_args,
            )
        else:
            # Use JDBC_DB_STRING for direct connection
            if not settings.JDBC_DB_STRING:
                raise RuntimeError("JDBC_DB_STRING not set but USE_CLOUD_SQL_PROXY is False")
            
            jdbc_params = parse_jdbc_connection_string(settings.JDBC_DB_STRING)
            print(f"[DEBUG] Parsed JDBC params: {jdbc_params}")  # Debug logging
            
            # If cloudSqlInstance is present, initialize connector first
            if jdbc_params['cloudSqlInstance']:
                print(f"[DEBUG] Initializing Cloud SQL Connector for instance: {jdbc_params['cloudSqlInstance']}")
                await init_connector()
                engine = _create_cloud_sql_engine(jdbc_params)
            else:
                print(f"[DEBUG] Using standard engine (no cloudSqlInstance found)")
                engine = _create_standard_engine(jdbc_params)
        
        # Create async session factory
        if engine:
            AsyncSessionLocal = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
            print(f"[DEBUG] AsyncSessionLocal created successfully: {AsyncSessionLocal is not None}")
        else:
            print("[ERROR] Engine is None after initialization!")
        
        _engine_initialized = True
        return engine
    except Exception as e:
        print(f"[ERROR] Failed to initialize database engine: {e}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise RuntimeError(f"Failed to initialize database engine: {e}")


async def get_db():
    """Dependency for getting database session"""
    if not AsyncSessionLocal:
        raise RuntimeError("Database not initialized. Call init_engine() first.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    # Ensure engine is initialized
    if not engine:
        await init_engine()
    
    if not engine:
        raise RuntimeError("Database engine could not be initialized.")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
