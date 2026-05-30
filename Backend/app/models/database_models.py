"""
Database Models for AeroGuard Application

This module defines all SQLAlchemy ORM models for the AeroGuard system.
These models work with PostgreSQL (Supabase/NeonDB) and define the database schema.

Models:
    - User: User accounts and authentication
    - Location: Geographic locations for AQI monitoring
    - Sensor: Physical or virtual sensors at locations
    - AQIData: Historical air quality measurements
    - Forecast: Predicted air quality values
    - UserLocation: Many-to-many relationship between users and locations
    - UserPreference: User-specific settings and preferences
    - ModelMetrics: Performance metrics for ML models
"""

from app.database import db
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum, Index


# ============================================================================
# Enums
# ============================================================================

class PersonaEnum(PyEnum):
    """User persona types for personalized recommendations"""
    GENERAL_PUBLIC = "general_public"
    HEALTH_SENSITIVE = "health_sensitive"
    OUTDOOR_ENTHUSIAST = "outdoor_enthusiast"
    PARENT = "parent"
    ELDERLY = "elderly"


# ============================================================================
# User Management Models
# ============================================================================

class User(db.Model):
    """
    User account model.
    
    Stores user authentication and profile information.
    Each user can have multiple favorite locations and preferences.
    
    Attributes:
        id (int): Primary key, auto-incremented
        email (str): Unique email address for login
        username (str): Unique username
        full_name (str): User's full name
        password_hash (str): Hashed password (not stored in plain text)
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last profile update timestamp
        is_active (bool): Account active status
        last_login (datetime): Last successful login time
    
    Relationships:
        locations: Favorite locations (many-to-many via UserLocation)
        preferences: User preferences (one-to-one)
    """
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Authentication Fields
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for OAuth users
    
    # Profile Information
    full_name = db.Column(db.String(255), nullable=True)
    
    # Account Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    locations = db.relationship('UserLocation', back_populates='user', cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', back_populates='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class UserPreference(db.Model):
    """
    User preferences and settings.
    
    Stores personalized settings for each user including alert thresholds,
    preferred forecast horizons, and persona type.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        persona (PersonaEnum): User persona type for recommendations
        alert_threshold_aqi (int): AQI level to trigger alerts
        preferred_forecast_hours (int): Default forecast horizon
        preferred_pollutants (str): Comma-separated list of pollutants to track
        notification_enabled (bool): Enable/disable notifications
        created_at (datetime): Preference creation time
        updated_at (datetime): Last update time
    """
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    # Persona & Preferences
    persona = db.Column(Enum(PersonaEnum), default=PersonaEnum.GENERAL_PUBLIC, nullable=False)
    alert_threshold_aqi = db.Column(db.Integer, default=100, nullable=False)
    preferred_forecast_hours = db.Column(db.Integer, default=6, nullable=False)
    preferred_pollutants = db.Column(db.String(255), default='pm25,pm10,aqi', nullable=False)
    notification_enabled = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='preferences')
    
    def __repr__(self):
        return f'<UserPreference user_id={self.user_id} persona={self.persona.value}>'


# ============================================================================
# Location & Sensor Models
# ============================================================================

class Location(db.Model):
    """
    Geographic location for AQI monitoring.
    
    Represents a city or area where air quality is monitored.
    Each location can have multiple sensors and historical data.
    
    Attributes:
        id (int): Primary key
        location_id (str): Unique identifier (e.g., 'delhi_central')
        city (str): City name
        country (str): Country name
        latitude (float): Geographic latitude
        longitude (float): Geographic longitude
        timezone (str): Timezone identifier
        created_at (datetime): Record creation time
    
    Relationships:
        sensors: Sensors at this location
        aqi_data: Historical AQI measurements
        forecasts: Forecast predictions
        users: Users who favorited this location
    """
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Geographic Information
    city = db.Column(db.String(255), nullable=False, index=True)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timezone = db.Column(db.String(50), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    sensors = db.relationship('Sensor', back_populates='location', cascade='all, delete-orphan')
    aqi_data = db.relationship('AQIData', back_populates='location', cascade='all, delete-orphan')
    forecasts = db.relationship('Forecast', back_populates='location', cascade='all, delete-orphan')
    users = db.relationship('UserLocation', back_populates='location', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Location {self.city}, {self.country}>'


class Sensor(db.Model):
    """
    Air quality sensor information.
    
    Represents physical or virtual sensors that collect AQI data.
    Each sensor is associated with a location.
    
    Attributes:
        id (int): Primary key
        sensor_id (str): Unique sensor identifier
        location_id (int): Foreign key to Location
        sensor_name (str): Human-readable sensor name
        latitude (float): Sensor latitude (may differ from location)
        longitude (float): Sensor longitude
        sensor_type (str): Type of sensor (e.g., 'PM2.5', 'Multi')
        provider (str): Data provider (e.g., 'WAQI', 'OpenAQ')
        is_active (bool): Sensor operational status
        last_reading_at (datetime): Last data received time
        created_at (datetime): Sensor registration time
    """
    __tablename__ = 'sensors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'), nullable=False)
    
    # Sensor Information
    sensor_name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)  # PM2.5, PM10, Multi, etc.
    provider = db.Column(db.String(100), nullable=True)  # WAQI, OpenAQ, etc.
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_reading_at = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    location = db.relationship('Location', back_populates='sensors')
    
    def __repr__(self):
        return f'<Sensor {self.sensor_name}>'


# ============================================================================
# AQI Data Models
# ============================================================================

class AQIData(db.Model):
    """
    Historical air quality measurements.
    
    Stores time-series data of air quality measurements including
    pollutant concentrations and meteorological data.
    
    Attributes:
        id (int): Primary key
        location_id (int): Foreign key to Location
        timestamp (datetime): Measurement timestamp
        pm25 (float): PM2.5 concentration (μg/m³)
        pm10 (float): PM10 concentration (μg/m³)
        aqi (float): Air Quality Index value
        temperature (float): Temperature (°C)
        humidity (float): Relative humidity (%)
        wind_speed (float): Wind speed (m/s)
        wind_direction (float): Wind direction (degrees)
        pressure (float): Atmospheric pressure (hPa)
        data_source (str): Source of data (e.g., 'WAQI', 'sensor')
        created_at (datetime): Record creation time
    
    Indexes:
        - (location_id, timestamp): For efficient time-series queries
        - timestamp: For date range queries
    """
    __tablename__ = 'aqi_data'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'), nullable=False)
    
    # Timestamp
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    
    # Pollutant Concentrations
    pm25 = db.Column(db.Float, nullable=True)  # PM2.5 in μg/m³
    pm10 = db.Column(db.Float, nullable=True)  # PM10 in μg/m³
    no2 = db.Column(db.Float, nullable=True)   # NO2 in μg/m³
    so2 = db.Column(db.Float, nullable=True)   # SO2 in μg/m³
    co = db.Column(db.Float, nullable=True)    # CO in μg/m³
    o3 = db.Column(db.Float, nullable=True)    # O3 in μg/m³
    
    # Composite AQI
    aqi = db.Column(db.Float, nullable=True)
    
    # Meteorological Data
    temperature = db.Column(db.Float, nullable=True)      # °C
    humidity = db.Column(db.Float, nullable=True)         # %
    wind_speed = db.Column(db.Float, nullable=True)       # m/s
    wind_direction = db.Column(db.Float, nullable=True)   # degrees
    pressure = db.Column(db.Float, nullable=True)         # hPa
    
    # Metadata
    data_source = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    location = db.relationship('Location', back_populates='aqi_data')
    
    # Composite index for efficient time-series queries
    __table_args__ = (
        Index('idx_location_timestamp', 'location_id', 'timestamp'),
    )
    
    def __repr__(self):
        return f'<AQIData location_id={self.location_id} timestamp={self.timestamp} aqi={self.aqi}>'


class Forecast(db.Model):
    """
    Air quality forecast predictions.
    
    Stores predicted air quality values generated by ML models.
    Each forecast includes confidence intervals and model metadata.
    
    Attributes:
        id (int): Primary key
        location_id (int): Foreign key to Location
        forecast_time (datetime): When forecast was generated
        forecast_date (date): Date being forecasted
        model_type (str): Model used (e.g., 'sarima', 'xgboost', 'ensemble')
        horizon_hours (int): Forecast horizon in hours
        aqi_forecast (float): Predicted AQI value
        pm25_forecast (float): Predicted PM2.5
        pm10_forecast (float): Predicted PM10
        confidence (float): Model confidence (0-1)
        prediction_interval_lower (float): Lower bound of prediction interval
        prediction_interval_upper (float): Upper bound of prediction interval
        created_at (datetime): Record creation time
    
    Indexes:
        - (location_id, forecast_date, model_type): For efficient forecast queries
    """
    __tablename__ = 'forecasts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'), nullable=False)
    
    # Forecast Metadata
    forecast_time = db.Column(db.DateTime, nullable=False)  # When forecast was made
    forecast_date = db.Column(db.Date, nullable=False, index=True)  # Date being forecasted
    model_type = db.Column(db.String(50), nullable=False)  # sarima, xgboost, lstm, ensemble
    horizon_hours = db.Column(db.Integer, nullable=False)  # Forecast horizon
    
    # Predictions
    aqi_forecast = db.Column(db.Float, nullable=True)
    pm25_forecast = db.Column(db.Float, nullable=True)
    pm10_forecast = db.Column(db.Float, nullable=True)
    no2_forecast = db.Column(db.Float, nullable=True)
    so2_forecast = db.Column(db.Float, nullable=True)
    co_forecast = db.Column(db.Float, nullable=True)
    o3_forecast = db.Column(db.Float, nullable=True)
    
    # Confidence & Intervals
    confidence = db.Column(db.Float, nullable=True)  # 0-1
    prediction_interval_lower = db.Column(db.Float, nullable=True)
    prediction_interval_upper = db.Column(db.Float, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    location = db.relationship('Location', back_populates='forecasts')
    
    # Composite index for efficient forecast queries
    __table_args__ = (
        Index('idx_location_forecast_model', 'location_id', 'forecast_date', 'model_type'),
    )
    
    def __repr__(self):
        return f'<Forecast location_id={self.location_id} date={self.forecast_date} model={self.model_type}>'


# ============================================================================
# Association & Metrics Models
# ============================================================================

class UserLocation(db.Model):
    """
    Many-to-many relationship between Users and Locations.
    
    Tracks which locations users have favorited and their
    location-specific alert preferences.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        location_id (int): Foreign key to Location
        is_favorite (bool): Whether location is favorited
        alert_threshold_aqi (int): Custom alert threshold for this location
        created_at (datetime): When location was added
    """
    __tablename__ = 'user_locations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'), nullable=False)
    
    # Preferences
    is_favorite = db.Column(db.Boolean, default=False, nullable=False)
    alert_threshold_aqi = db.Column(db.Integer, default=100, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='locations')
    location = db.relationship('Location', back_populates='users')
    
    # Ensure unique user-location pairs
    __table_args__ = (
        db.UniqueConstraint('user_id', 'location_id', name='uq_user_location'),
    )
    
    def __repr__(self):
        return f'<UserLocation user_id={self.user_id} location_id={self.location_id}>'


class ModelMetrics(db.Model):
    """
    Performance metrics for ML models.
    
    Tracks accuracy and performance metrics for different forecasting
    models at different locations and time horizons.
    
    Attributes:
        id (int): Primary key
        model_type (str): Model identifier (e.g., 'sarima', 'xgboost')
        location_id (int): Foreign key to Location (optional)
        evaluation_date (date): Date of evaluation
        mae (float): Mean Absolute Error
        rmse (float): Root Mean Squared Error
        mape (float): Mean Absolute Percentage Error
        r2_score (float): R² Score
        samples_count (int): Number of samples evaluated
        forecast_hours (int): Forecast horizon evaluated
        training_data_days (int): Days of training data used
        created_at (datetime): Record creation time
    
    Indexes:
        - (model_type, location_id, evaluation_date): For metric queries
    """
    __tablename__ = 'model_metrics'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_type = db.Column(db.String(50), nullable=False, index=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='SET NULL'), nullable=True)
    
    # Evaluation Metadata
    evaluation_date = db.Column(db.Date, nullable=False, index=True)
    forecast_hours = db.Column(db.Integer, nullable=False)
    training_data_days = db.Column(db.Integer, nullable=True)
    samples_count = db.Column(db.Integer, nullable=False)
    
    # Performance Metrics
    mae = db.Column(db.Float, nullable=True)   # Mean Absolute Error
    rmse = db.Column(db.Float, nullable=True)  # Root Mean Squared Error
    mape = db.Column(db.Float, nullable=True)  # Mean Absolute Percentage Error
    r2_score = db.Column(db.Float, nullable=True)  # R² Score
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Composite index for efficient metric queries
    __table_args__ = (
        Index('idx_model_location_date', 'model_type', 'location_id', 'evaluation_date'),
    )
    
    def __repr__(self):
        return f'<ModelMetrics model={self.model_type} date={self.evaluation_date} rmse={self.rmse}>'
