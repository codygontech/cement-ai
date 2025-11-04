"""
Google Cloud Vision API Integration
Provides quality inspection and defect detection capabilities
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import io

from google.cloud import vision
from google.cloud import storage
from PIL import Image

from app.core.config import settings
from app.core.logging_config import logger
from app.db import session as db_session
from sqlalchemy import text

router = APIRouter()

# Initialize Vision API client
try:
    vision_client = vision.ImageAnnotatorClient()
    storage_client = storage.Client(project=settings.GOOGLE_CLOUD_PROJECT)
except Exception as e:
    logger.warning(f"Failed to initialize Google Cloud clients: {e}")
    vision_client = None
    storage_client = None


class VisionAnalysisResult(BaseModel):
    """Vision analysis result model"""
    image_url: str
    defects_detected: List[str]
    confidence_score: float
    quality_score: float
    labels: List[str]
    analysis_timestamp: str
    recommendations: List[str]


class QualityInspectionRequest(BaseModel):
    """Quality inspection request"""
    sample_id: str
    process_stage: str  # raw_material, clinker, cement


@router.post("/analyze", response_model=VisionAnalysisResult)
async def analyze_image(
    file: UploadFile = File(...),
    sample_id: Optional[str] = None
):
    """
    Analyze cement quality using Google Cloud Vision API
    Detects defects, cracks, color variations, and quality issues
    """
    try:
        if not vision_client:
            raise HTTPException(
                status_code=503,
                detail="Google Cloud Vision API is not configured"
            )
        
        # Read image file
        image_data = await file.read()
        image = vision.Image(content=image_data)
        
        # Perform multiple vision analyses
        # 1. Label detection for general characteristics
        label_response = vision_client.label_detection(image=image)
        labels = [label.description for label in label_response.label_annotations[:10]]
        
        # 2. Object detection for defect identification
        object_response = vision_client.object_localization(image=image)
        detected_objects = [
            {
                "name": obj.name,
                "confidence": obj.score,
                "bounds": [(vertex.x, vertex.y) for vertex in obj.bounding_poly.normalized_vertices]
            }
            for obj in object_response.localized_object_annotations
        ]
        
        # 3. Image properties for color analysis
        props_response = vision_client.image_properties(image=image)
        dominant_colors = props_response.image_properties_annotation.dominant_colors.colors[:3]
        
        # Analyze for cement-specific quality indicators
        defects = []
        quality_score = 100.0
        
        # Check for common cement defects based on vision analysis
        defect_keywords = ["crack", "void", "segregation", "discolor", "contamination", "lump"]
        for label in labels:
            for keyword in defect_keywords:
                if keyword.lower() in label.lower():
                    defects.append(f"Potential {keyword} detected: {label}")
                    quality_score -= 15
        
        # Color consistency check for cement
        # Cement should have consistent gray color
        color_variance = sum(
            abs(color.color.red - 150) + abs(color.color.green - 150) + abs(color.color.blue - 150)
            for color in dominant_colors
        ) / len(dominant_colors) if dominant_colors else 0
        
        if color_variance > 100:
            defects.append(f"Color inconsistency detected (variance: {color_variance:.1f})")
            quality_score -= 10
        
        # Calculate confidence score
        avg_confidence = sum(obj["confidence"] for obj in detected_objects) / len(detected_objects) if detected_objects else 0.85
        confidence_score = min(0.95, avg_confidence + 0.1)
        
        # Generate recommendations
        recommendations = []
        if quality_score < 70:
            recommendations.append("Quality inspection required - multiple defects detected")
        if color_variance > 100:
            recommendations.append("Check raw material consistency and grinding parameters")
        if len(defects) > 2:
            recommendations.append("Investigate process parameters and quality control procedures")
        if not defects:
            recommendations.append("Quality within acceptable range - continue monitoring")
        
        # Upload image to Cloud Storage if configured
        image_url = ""
        if storage_client and settings.GCS_IMAGES_BUCKET:
            try:
                bucket = storage_client.bucket(settings.GCS_IMAGES_BUCKET)
                blob_name = f"inspections/{datetime.now().strftime('%Y%m%d')}/{sample_id or 'sample'}_{datetime.now().timestamp()}.jpg"
                blob = bucket.blob(blob_name)
                blob.upload_from_string(image_data, content_type=file.content_type)
                image_url = f"gs://{settings.GCS_IMAGES_BUCKET}/{blob_name}"
            except Exception as e:
                logger.warning(f"Failed to upload image to Cloud Storage: {e}")
                image_url = "local_storage"
        
        # Save results to database
        try:
            async with db_session.AsyncSessionLocal() as session:
                await session.execute(
                    text("""
                        INSERT INTO quality_metrics 
                        (sample_id, vision_inspection_score, defect_detected, timestamp)
                        VALUES (:sample_id, :score, :defect, NOW())
                    """),
                    {
                        "sample_id": sample_id or f"vision_{datetime.now().timestamp()}",
                        "score": quality_score,
                        "defect": len(defects) > 0
                    }
                )
                await session.commit()
        except Exception as e:
            logger.warning(f"Failed to save vision results: {e}")
        
        return VisionAnalysisResult(
            image_url=image_url,
            defects_detected=defects,
            confidence_score=round(confidence_score, 3),
            quality_score=round(quality_score, 2),
            labels=labels,
            analysis_timestamp=datetime.now().isoformat(),
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-analyze")
async def batch_analyze_images(files: List[UploadFile] = File(...)):
    """
    Analyze multiple images in batch
    """
    results = []
    
    for file in files:
        try:
            result = await analyze_image(file)
            results.append(result)
        except Exception as e:
            logger.error(f"Error analyzing {file.filename}: {e}")
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "total_images": len(files),
        "results": results,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/inspection-history")
async def get_inspection_history(days: int = 7, limit: int = 100):
    """
    Get vision inspection history
    """
    try:
        async with db_session.AsyncSessionLocal() as session:
            result = await session.execute(
                text("""
                    SELECT 
                        sample_id,
                        vision_inspection_score,
                        defect_detected,
                        timestamp
                    FROM quality_metrics
                    WHERE vision_inspection_score IS NOT NULL
                    AND timestamp >= NOW() - INTERVAL ':days days'
                    ORDER BY timestamp DESC
                    LIMIT :limit
                """),
                {"days": days, "limit": limit}
            )
            
            rows = result.fetchall()
            
            history = [
                {
                    "sample_id": row[0],
                    "quality_score": row[1],
                    "defect_detected": row[2],
                    "timestamp": row[3].isoformat() if row[3] else None
                }
                for row in rows
            ]
            
            return {
                "period_days": days,
                "inspections": history,
                "total_count": len(history)
            }
            
    except Exception as e:
        logger.error(f"Error fetching inspection history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
