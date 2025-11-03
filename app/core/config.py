"""
Core configuration for JK Cement AI Optimization System
Manages all Google Cloud services and API settings for JK Cement India operations
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings with Google Cloud integration for JK Cement India"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Google Cloud Configuration
    GOOGLE_CLOUD_PROJECT: str = "jk-cement-ai-optimization"
    GOOGLE_API_KEY: str = ""
    
    # Vertex AI Configuration
    VERTEX_AI_LOCATION: str = "asia-south1"  # Mumbai region for JK Cement India
    VERTEX_AI_MODEL: str = "gemini-2.0-flash-exp"
    
    # Database Configuration
    DATABASE_URL: str = ""  # For Cloud SQL Proxy: postgresql+asyncpg://user:pass@localhost:5432/dbname
    JDBC_DB_STRING: str = ""  # For direct Cloud SQL: jdbc:postgresql:///dbname?cloudSqlInstance=project:region:instance
    DATABASE_USER: str = ""
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = ""
    USE_CLOUD_SQL_PROXY: bool = False  # True = use DATABASE_URL, False = use JDBC_DB_STRING
    
    # Cloud Storage
    GCS_IMAGES_BUCKET: str = "jk-cement-plant-images"
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    PORT: int | None = None  # Cloud Run sets this automatically
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # Logging
    ENABLE_CLOUD_LOGGING: bool = False
    LOG_LEVEL: str = "INFO"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string or list"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS
    
    @property
    def server_port(self) -> int:
        """Get the port to use, preferring Cloud Run's PORT if set"""
        return self.PORT if self.PORT is not None else self.API_PORT


settings = Settings()
