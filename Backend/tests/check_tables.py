"""
Check what tables exist and in which schema
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import DevelopmentConfig
from app import create_app
from sqlalchemy import inspect, text

def check_tables():
    """Check all tables in the database"""
    app = create_app(DevelopmentConfig)
    
    with app.app_context():
        from app.database import db
        
        print("\n" + "="*70)
        print("CHECKING TABLES IN DATABASE")
        print("="*70 + "\n")
        
        # Get the inspector
        inspector = inspect(db.engine)
        
        # Check all schemas
        print("📋 Checking all schemas...\n")
        
        # Get tables in public schema
        public_tables = inspector.get_table_names(schema='public')
        print(f"✅ Tables in 'public' schema: {len(public_tables)}")
        for table in sorted(public_tables):
            print(f"   - {table}")
        
        # Try to get all schemas
        print("\n🔍 Checking for other schemas...")
        try:
            result = db.session.execute(text("""
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
                ORDER BY schema_name;
            """))
            schemas = [row[0] for row in result]
            print(f"   Found schemas: {', '.join(schemas)}")
            
            # Check tables in each schema
            for schema in schemas:
                if schema != 'public':
                    tables = inspector.get_table_names(schema=schema)
                    if tables:
                        print(f"\n   Tables in '{schema}' schema: {len(tables)}")
                        for table in sorted(tables):
                            print(f"      - {table}")
        except Exception as e:
            print(f"   Could not check schemas: {e}")
        
        # Check if our models' tables exist
        print("\n" + "="*70)
        print("CHECKING EXPECTED TABLES")
        print("="*70 + "\n")
        
        expected_tables = [
            'users', 'user_preferences', 'locations', 'sensors',
            'aqi_data', 'forecasts', 'user_locations', 'model_metrics'
        ]
        
        for table in expected_tables:
            exists = inspector.has_table(table, schema='public')
            status = "✅" if exists else "❌"
            print(f"{status} {table}")
        
        # Show connection info
        print("\n" + "="*70)
        print("CONNECTION INFO")
        print("="*70 + "\n")
        
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        if '@' in db_url:
            host = db_url.split('@')[1].split('/')[0]
            database = db_url.split('/')[-1].split('?')[0]
            print(f"🔗 Host: {host}")
            print(f"🗄️  Database: {database}")
            
            if 'supabase' in db_url:
                print(f"✅ Provider: Supabase")
            elif 'neon' in db_url:
                print(f"⚠️  Provider: NeonDB")

if __name__ == "__main__":
    check_tables()
