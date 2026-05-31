"""
Check which database we're actually connected to
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the DATABASE_URL
db_url = os.getenv('DATABASE_URL')

print("\n" + "="*70)
print("DATABASE CONNECTION CHECK")
print("="*70 + "\n")

# print(f"DATABASE_URL from .env file:")
# print(f"{db_url}\n")

# Parse the connection string
if db_url:
    parts = db_url.split('@')
    if len(parts) > 1:
        host_part = parts[1].split('/')[0]
        print(f"🔍 Host: {host_part}")
        
        if 'supabase' in db_url:
            print("✅ Connected to: SUPABASE")
        elif 'neon' in db_url:
            print("⚠️  Connected to: NEONDB (old database)")
        else:
            print("❓ Connected to: UNKNOWN")
    
    # Check if it's the pooler or direct connection
    if 'pooler.supabase.com' in db_url:
        print("📡 Connection type: Pooler (recommended)")
    elif 'db.supabase.co' in db_url:
        print("📡 Connection type: Direct")
else:
    print("❌ No DATABASE_URL found!")

print("\n" + "="*70)
