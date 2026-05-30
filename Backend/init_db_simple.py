"""
Simple database initialization script for Supabase migration
"""
import os
import sys
from pathlib import Path

# Set environment to development
os.environ['FLASK_ENV'] = 'development'

# Add Backend to path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask
from app.database import db
from app.models.database_models import (
    User, Location, Sensor, AQIData, Forecast, 
    UserLocation, UserPreference, ModelMetrics, PersonaEnum
)

def init_database():
    """Initialize database with Supabase connection"""
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        print("Make sure your .env file is in the Backend directory")
        return False
    
    print("\n" + "="*70)
    print("SUPABASE DATABASE INITIALIZATION")
    print("="*70)
    print(f"\n📍 Connecting to: {database_url.split('@')[1].split('/')[0]}...")
    
    # Create minimal Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_size": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "connect_args": {"connect_timeout": 10},
    }
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        try:
            # Test connection
            db.engine.connect()
            print("✅ Database connection successful!")
            
            # Create all tables
            print("\n📊 Creating tables...")
            db.create_all()
            
            # List created tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n✅ Successfully created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"   • {table}")
            
            print("\n" + "="*70)
            print("✅ DATABASE INITIALIZATION COMPLETE!")
            print("="*70)
            print("\n💡 Next steps:")
            print("   1. Check Supabase Dashboard → Table Editor")
            print("   2. Run: python init_db_simple.py --seed (to add sample data)")
            print("   3. Run: python run.py (to start your backend)")
            print()
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            print("\n🔍 Troubleshooting:")
            print("   1. Check your DATABASE_URL in .env file")
            print("   2. Verify your Supabase password is correct")
            print("   3. Ensure your Supabase project is active")
            print()
            return False

def seed_sample_data():
    """Add sample data for testing"""
    from datetime import datetime, timedelta
    
    database_url = os.getenv('DATABASE_URL')
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        print("\n" + "="*70)
        print("SEEDING SAMPLE DATA")
        print("="*70)
        
        try:
            # Create sample users
            print("\n👤 Creating sample users...")
            user1 = User(
                email="alice@example.com",
                username="alice",
                full_name="Alice Johnson"
            )
            user2 = User(
                email="bob@example.com",
                username="bob",
                full_name="Bob Smith"
            )
            db.session.add_all([user1, user2])
            db.session.commit()
            print("   ✅ Created 2 users")
            
            # Create sample locations
            print("\n📍 Creating sample locations...")
            locations_data = [
                {
                    "city": "Delhi",
                    "country": "India",
                    "latitude": 28.7041,
                    "longitude": 77.1025,
                    "location_id": "delhi_central"
                },
                {
                    "city": "Mumbai",
                    "country": "India",
                    "latitude": 19.0760,
                    "longitude": 72.8777,
                    "location_id": "mumbai_central"
                },
                {
                    "city": "Bangalore",
                    "country": "India",
                    "latitude": 12.9716,
                    "longitude": 77.5946,
                    "location_id": "bangalore_central"
                },
            ]
            
            locations = []
            for loc_data in locations_data:
                loc = Location(**loc_data)
                locations.append(loc)
                db.session.add(loc)
            db.session.commit()
            print(f"   ✅ Created {len(locations)} locations")
            
            # Create sample sensors
            print("\n🔬 Creating sample sensors...")
            for location in locations:
                sensor = Sensor(
                    location_id=location.id,
                    sensor_id=f"{location.location_id}_sensor_1",
                    sensor_name=f"AQI Monitor - {location.city}",
                    latitude=location.latitude,
                    longitude=location.longitude,
                    sensor_type="Multi",
                    provider="WAQI"
                )
                db.session.add(sensor)
            db.session.commit()
            print(f"   ✅ Created sensors for all locations")
            
            # Create sample AQI data (last 7 days)
            print("\n📈 Creating sample AQI data...")
            aqi_count = 0
            for location in locations:
                for days_back in range(7):
                    for hour in range(0, 24, 6):  # 4 measurements per day
                        timestamp = datetime.utcnow() - timedelta(days=days_back, hours=hour)
                        aqi_data = AQIData(
                            location_id=location.id,
                            timestamp=timestamp,
                            pm25=40 + (days_back % 10) * 5,
                            pm10=60 + (days_back % 10) * 7,
                            aqi=50 + (days_back % 10) * 8,
                            temperature=20 + (hour // 6) * 5,
                            humidity=60 + (hour % 6) * 5,
                            wind_speed=2 + (hour % 4),
                            data_source="sample"
                        )
                        db.session.add(aqi_data)
                        aqi_count += 1
            db.session.commit()
            print(f"   ✅ Created {aqi_count} AQI data points")
            
            # Create user preferences
            print("\n⚙️  Creating user preferences...")
            for user in [user1, user2]:
                pref = UserPreference(
                    user_id=user.id,
                    persona=PersonaEnum.GENERAL_PUBLIC,
                    alert_threshold_aqi=100,
                    preferred_forecast_hours=6,
                    preferred_pollutants="pm25,pm10,aqi"
                )
                db.session.add(pref)
            db.session.commit()
            print("   ✅ Created user preferences")
            
            print("\n" + "="*70)
            print("✅ SAMPLE DATA SEEDED SUCCESSFULLY!")
            print("="*70)
            print()
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR: {e}")
            raise

if __name__ == "__main__":
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check for --seed flag
    if len(sys.argv) > 1 and sys.argv[1] == '--seed':
        seed_sample_data()
    else:
        init_database()
