"""
Test adding new data to Supabase
"""
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from app.config import DevelopmentConfig
from app import create_app
from app.database import db
from app.models.database_models import Location, AQIData

def test_add_data():
    """Add a new location and AQI data to Supabase"""
    app = create_app(DevelopmentConfig)
    
    with app.app_context():
        print("\n" + "="*70)
        print("TESTING: Adding New Data to Supabase")
        print("="*70 + "\n")
        
        # Check if Mumbai already exists
        mumbai = Location.query.filter_by(city='Mumbai').first()
        
        if not mumbai:
            # Add new location
            print("➕ Adding new location: Mumbai, India")
            mumbai = Location(
                city='Mumbai',
                country='India',
                latitude=19.0760,
                longitude=72.8777,
                location_id='mumbai_central'
            )
            db.session.add(mumbai)
            db.session.commit()
            print(f"✅ Location added! ID: {mumbai.id}")
        else:
            print(f"ℹ️  Mumbai already exists (ID: {mumbai.id})")
        
        # Add new AQI data for Mumbai
        print("\n➕ Adding new AQI data for Mumbai")
        new_aqi = AQIData(
            location_id=mumbai.id,
            timestamp=datetime.utcnow(),
            pm25=55.5,
            pm10=85.2,
            aqi=145.0,
            temperature=28.5,
            humidity=75.0,
            wind_speed=3.2,
            data_source='test_script'
        )
        db.session.add(new_aqi)
        db.session.commit()
        print(f"✅ AQI data added! ID: {new_aqi.id}")
        
        # Verify the data
        print("\n" + "="*70)
        print("VERIFICATION: Reading Back from Supabase")
        print("="*70 + "\n")
        
        # Count total locations
        total_locations = Location.query.count()
        print(f"📍 Total Locations in Supabase: {total_locations}")
        
        # Get Mumbai data
        mumbai_data = AQIData.query.filter_by(location_id=mumbai.id).order_by(AQIData.timestamp.desc()).first()
        print(f"\n🌆 Latest Mumbai AQI Data:")
        print(f"   - AQI: {mumbai_data.aqi}")
        print(f"   - PM2.5: {mumbai_data.pm25}")
        print(f"   - PM10: {mumbai_data.pm10}")
        print(f"   - Temperature: {mumbai_data.temperature}°C")
        print(f"   - Timestamp: {mumbai_data.timestamp}")
        
        print("\n" + "="*70)
        print("✅ SUCCESS! Data is being stored in Supabase!")
        print("="*70)
        print("\n💡 Go to Supabase Dashboard → Table Editor to see this data!")
        print("   - Check 'locations' table for Mumbai")
        print("   - Check 'aqi_data' table for the new AQI reading\n")

if __name__ == "__main__":
    test_add_data()
