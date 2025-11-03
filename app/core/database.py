"""
Database models and tables for Cement Plant AI
Aligned with actual Cloud SQL database schema
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, Text, Boolean, JSON, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class RawMaterialFeed(Base):
    """Raw material feed data - matches actual DB schema"""
    __tablename__ = "raw_material_feed"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    limestone_qty = Column(Numeric)
    clay_qty = Column(Numeric)
    iron_ore_qty = Column(Numeric)
    gypsum_qty = Column(Numeric)
    total_feed_rate = Column(Numeric)
    moisture_content = Column(Numeric)
    lsf = Column(Numeric)
    sm = Column(Numeric)
    am = Column(Numeric)


class KilnOperations(Base):
    """Kiln operations data - matches actual DB schema"""
    __tablename__ = "kiln_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    feed_rate = Column(Numeric)
    kiln_speed = Column(Numeric)
    burning_zone_temp = Column(Numeric)
    coal_feed_rate = Column(Numeric)
    alternative_fuel_rate = Column(Numeric)
    o2_pct = Column(Numeric)
    co_ppm = Column(Integer)
    nox_ppm = Column(Integer)
    clinker_production = Column(Numeric)
    free_lime = Column(Numeric)
    thermal_consumption = Column(Numeric)


class GrindingOperations(Base):
    """Grinding operations data - matches actual DB schema"""
    __tablename__ = "grinding_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    mill_id = Column(String(255))  # Changed from mill_type to mill_id
    feed_rate = Column(Numeric)
    mill_speed = Column(Numeric)
    separator_speed = Column(Numeric)
    power_consumption = Column(Numeric)
    product_fineness = Column(Numeric)  # Changed from blaine_fineness
    residue_45_micron = Column(Numeric)
    temperature = Column(Numeric)  # New field in actual DB


class QualityControl(Base):
    """Quality control metrics - matches actual DB schema (renamed from QualityMetrics)"""
    __tablename__ = "quality_control"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    sample_type = Column(String(255))  # Changed from sample_id
    compressive_strength_3d = Column(Numeric)
    compressive_strength_7d = Column(Numeric)
    compressive_strength_28d = Column(Numeric)
    setting_time_initial = Column(Integer)  # New field in actual DB
    setting_time_final = Column(Integer)  # New field in actual DB
    fineness = Column(Numeric)  # New field in actual DB
    so3 = Column(Numeric)  # Changed from so3_content
    loss_on_ignition = Column(Numeric)
    status = Column(String(255))  # New field in actual DB


class AIRecommendations(Base):
    """AI-generated recommendations - matches actual DB schema"""
    __tablename__ = "ai_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    category = Column(String(255))  # Changed from module
    title = Column(Text)  # New field in actual DB
    description = Column(Text)
    priority = Column(String(255))
    expected_impact = Column(Text)  # Changed from estimated_savings
    status = Column(String(255))
    implementation_date = Column(DateTime(timezone=False))  # New field in actual DB
    feedback = Column(Text)  # New field in actual DB


class AlternativeFuels(Base):
    """Alternative fuels data - new table from actual DB"""
    __tablename__ = "alternative_fuels"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    fuel_type = Column(String(255))
    quantity = Column(Numeric)
    calorific_value = Column(Numeric)
    cost_per_ton = Column(Numeric)
    co2_emission_factor = Column(Numeric)
    tsr = Column(Numeric)  # Thermal Substitution Rate
    savings_amount = Column(Numeric)


class OptimizationResults(Base):
    """Optimization results - new table from actual DB"""
    __tablename__ = "optimization_results"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    optimization_type = Column(String(255))
    parameter_name = Column(String(255))
    current_value = Column(Numeric)
    recommended_value = Column(Numeric)
    expected_savings = Column(Numeric)
    confidence_score = Column(Numeric)
    implementation_status = Column(String(255))
    actual_savings = Column(Numeric)


class UtilitiesMonitoring(Base):
    """Utilities monitoring - new table from actual DB"""
    __tablename__ = "utilities_monitoring"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    power_consumption = Column(Numeric)
    specific_power = Column(Numeric)
    water_consumption = Column(Numeric)
    compressed_air_pressure = Column(Numeric)
    thermal_energy = Column(Numeric)
    cost_per_ton = Column(Numeric)


class PlantLocations(Base):
    """Plant locations - new table from actual DB"""
    __tablename__ = "plant_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    plant_code = Column(String(255), nullable=False)
    plant_name = Column(String(255), nullable=False)
    location = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    country = Column(String(255))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacity_tpd = Column(Integer)  # Tons per day
    plant_type = Column(String(255))
    commissioned_year = Column(Integer)
    status = Column(String(255), default='operational')
    contact_email = Column(String(255))
    contact_phone = Column(String(255))
    description = Column(Text)
    meta_data = Column('metadata', JSONB)  # Map to 'metadata' column in DB
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())


class ChatHistory(Base):
    """AI chatbot conversation history - model for future table"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    role = Column(String(20))  # user, assistant, system
    content = Column(Text)
    tool_calls = Column(JSON)
    meta_data = Column(JSON)

