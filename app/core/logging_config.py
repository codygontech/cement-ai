"""
Google Cloud Logging configuration for JK Cement AI
"""

import logging
import sys
from app.core.config import settings

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("jk_cement_ai")

# Initialize Google Cloud Logging if enabled
if settings.ENABLE_CLOUD_LOGGING and settings.GOOGLE_CLOUD_PROJECT:
    try:
        from google.cloud import logging as cloud_logging
        
        client = cloud_logging.Client(project=settings.GOOGLE_CLOUD_PROJECT)
        client.setup_logging()
        logger.info("Google Cloud Logging initialized for JK Cement AI")
    except Exception as e:
        logger.warning(f"Failed to initialize Google Cloud Logging: {e}")
