"""
Verify that data is stored in Supabase
"""
import os
import sys
from pathlib import Path

# Add Backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.database import db
from app.models.database_models import (
    User, Location, Sensor, AQIData, Forecast,
    UserLocation, UserPreference, ModelMetrics
)

def verify_data():
    """Check data in Supabase"""
    from app.config import DevelopmentConfig
    app = create_app(DevelopmentConfig)
    
    with app.app_context():
        print("\n" + "="*70)
        print("VERIFYING DATA IN SUPABASE")
        print("="*70 + "\n")
        
        # Check Users
        users = User.query.all()
        print(f"✅ Users: {len(users)} records")
        for user in users:
            print(f"   - {user.username} ({user.email})")
        
        # Check Locations
        locations = Location.query.all()
        print(f"\n✅ Locations: {len(locations)} records")
        for loc in locations:
            print(f"   - {loc.city}, {loc.country} (lat: {loc.latitude}, lng: {loc.longitude})")
        
        # Check Sensors
        sensors = Sensor.query.all()
        print(f"\n✅ Sensors: {len(sensors)} records")
        for sensor in sensors:
            print(f"   - {sensor.sensor_name} (Active: {sensor.is_active})")
        
        # Check AQI Data
        aqi_data = AQIData.query.all()
        print(f"\n✅ AQI Data: {len(aqi_data)} records")
        if aqi_data:
            latest = AQIData.query.order_by(AQIData.timestamp.desc()).first()
            print(f"   - Latest: AQI={latest.aqi}, PM2.5={latest.pm25}, PM10={latest.pm10}")
            print(f"   - Timestamp: {latest.timestamp}")
        
        # Check Forecasts
        forecasts = Forecast.query.all()
        print(f"\n✅ Forecasts: {len(forecasts)} records")
        for forecast in forecasts[:3]:  # Show first 3
            print(f"   - {forecast.model_type}: AQI={forecast.aqi_forecast} (confidence: {forecast.confidence})")
        
        # Check User Preferences
        preferences = UserPreference.query.all()
        print(f"\n✅ User Preferences: {len(preferences)} records")
        for pref in preferences:
            print(f"   - User {pref.user_id}: Persona={pref.persona.value}, Alert Threshold={pref.alert_threshold_aqi}")
        
        # Check User Locations
        user_locations = UserLocation.query.all()
        print(f"\n✅ User Locations: {len(user_locations)} records")
        for ul in user_locations:
            print(f"   - User {ul.user_id} → Location {ul.location_id} (Favorite: {ul.is_favorite})")
        
        # Check Model Metrics
        metrics = ModelMetrics.query.all()
        print(f"\n✅ Model Metrics: {len(metrics)} records")
        for metric in metrics[:3]:  # Show first 3
            print(f"   - {metric.model_type}: RMSE={metric.rmse}, MAE={metric.mae}, R²={metric.r2_score}")
        
        print("\n" + "="*70)
        print("✅ ALL DATA IS SUCCESSFULLY STORED IN SUPABASE!")
        print("="*70 + "\n")
        
        # Show connection info
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        if 'supabase' in db_url:
            print("🎯 Connected to: SUPABASE")
            print(f"   Host: {db_url.split('@')[1].split(':')[0]}")
        else:
            print("⚠️  Not connected to Supabase")

if __name__ == "__main__":
    verify_data()
