"""
Verify tables exist in Supabase using direct PostgreSQL connection
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')

print("\n" + "="*70)
print("VERIFYING TABLES IN SUPABASE")
print("="*70 + "\n")

try:
    # Connect directly to PostgreSQL
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    # Get all tables in public schema
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    
    print(f"✅ Found {len(tables)} tables in Supabase:\n")
    
    for (table_name,) in tables:
        # Get row count for each table
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        count = cursor.fetchone()[0]
        print(f"   📊 {table_name}: {count} rows")
    
    print("\n" + "="*70)
    print("✅ TABLES ARE IN SUPABASE!")
    print("="*70)
    print("\n💡 Go to Supabase Dashboard → Table Editor to see these tables\n")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure:")
    print("1. DATABASE_URL in .env points to Supabase")
    print("2. Supabase project is active")
    print("3. Connection string is correct")
