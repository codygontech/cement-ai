"""
JK Cement AI Optimization System - Backend API
Google Cloud Integration with Vertex AI, Cloud SQL, Cloud Storage, and Cloud Vision
Optimized for JK Cement India operations
"""

import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.server_port,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
