# 🚀 Supabase Migration Guide for AeroGuard

## 📌 Overview

**Good News!** Your application is already using PostgreSQL (NeonDB), so migrating to Supabase is straightforward. Supabase is also PostgreSQL-based, which means:
- ✅ No code changes needed
- ✅ Same SQL syntax
- ✅ Same SQLAlchemy models work perfectly
- ✅ Just change the connection string!

---

## 🎯 Why Migrate to Supabase?

| Feature | NeonDB | Supabase |
|---------|--------|----------|
| **Database** | PostgreSQL ✅ | PostgreSQL ✅ |
| **Free Tier** | 0.5 GB storage | 500 MB storage |
| **Built-in Auth** | ❌ | ✅ (Email, OAuth, Magic Links) |
| **Real-time** | ❌ | ✅ (WebSocket subscriptions) |
| **Storage** | ❌ | ✅ (File storage built-in) |
| **Auto APIs** | ❌ | ✅ (REST & GraphQL auto-generated) |
| **Dashboard** | Basic | Advanced with SQL Editor |
| **Backups** | Limited | Daily automatic backups |

---

## 📋 Step-by-Step Migration Process

### **Step 1: Create Supabase Project** (5 minutes)

1. **Go to Supabase**
   - Visit: https://supabase.com
   - Click "Start your project" or "Sign In"

2. **Create New Project**
   - Click "New Project"
   - Fill in details:
     ```
     Name: AeroGuard
     Database Password: [Create a strong password - SAVE THIS!]
     Region: [Choose closest to your users, e.g., US East, EU West]
     Pricing Plan: Free
     ```
   - Click "Create new project"
   - Wait ~2 minutes for provisioning

3. **Save Your Credentials**
   ```
   Project URL: https://xxxxx.supabase.co
   API Key (anon): eyJhbGc...
   Database Password: [Your password]
   ```

---

### **Step 2: Get Supabase Connection String** (2 minutes)

1. **Navigate to Database Settings**
   - In Supabase Dashboard, click **Settings** (⚙️ icon in sidebar)
   - Click **Database**

2. **Copy Connection String**
   - Scroll to **Connection String** section
   - Select **URI** tab (not Session mode)
   - You'll see something like:
     ```
     postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
     ```
   - **IMPORTANT**: Replace `[YOUR-PASSWORD]` with your actual database password

3. **Example Connection String**
   ```
   postgresql://postgres.abcdefghijklmnop:MySecurePass123!@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

---

### **Step 3: Update Your .env File** (1 minute)

1. **Open** `Backend/.env`

2. **Replace the DATABASE_URL line** with your Supabase connection string:

   ```env
   # OLD (NeonDB)
   # DATABASE_URL=postgresql://neondb_owner:xxxxx@ep-xxx.aws.neon.tech/neondb?sslmode=require

   # NEW (Supabase)
   DATABASE_URL=postgresql://postgres.xxxxx:YourPassword@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

3. **Save the file**

---

### **Step 4: Initialize Supabase Database** (2 minutes)

Now we'll create all the tables in your new Supabase database.

1. **Open Terminal** in your Backend directory:
   ```bash
   cd "d:\VS-Code projects\AeroGuard_\Backend"
   ```

2. **Activate your Python virtual environment** (if you have one):
   ```bash
   # Windows
   venv\Scripts\activate

   # Or if using conda
   conda activate aeroguard
   ```

3. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements-fixed.txt
   ```

4. **Initialize the database**:
   ```bash
   python init_db.py
   ```

   **Expected Output:**
   ```
   ======================================================================
   DATABASE INITIALIZATION
   ======================================================================
   ✓ Database initialized (existing SQLAlchemy instance)
   ```

5. **Seed with sample data** (optional, for testing):
   ```bash
   python init_db.py --seed
   ```

   **Expected Output:**
   ```
   ======================================================================
   SEEDING SAMPLE DATA
   ======================================================================

   Creating sample users...
   ✓ Created 2 users

   Creating sample locations...
   ✓ Created 3 locations

   Creating sample sensors...
   ✓ Created sensors for all locations

   Creating sample AQI data...
   ✓ Created 360 AQI data points

   Creating sample forecasts...
   ✓ Created 9 forecasts

   Creating sample user preferences...
   ✓ Created user preferences

   Creating sample user locations...
   ✓ Created user location mappings

   Creating model metrics...
   ✓ Created model metrics

   ======================================================================
   ✓ Sample data seeded successfully!
   ======================================================================
   ```

---

### **Step 5: Verify Migration** (3 minutes)

1. **Check Supabase Dashboard**
   - Go to Supabase Dashboard
   - Click **Table Editor** in sidebar
   - You should see all your tables:
     - `users`
     - `locations`
     - `sensors`
     - `aqi_data`
     - `forecasts`
     - `user_preferences`
     - `user_locations`
     - `model_metrics`

2. **Test Your Backend**
   ```bash
   python run.py
   ```

   **Expected Output:**
   ```
   * Running on http://0.0.0.0:5000
   * Debug mode: on
   ```

3. **Test API Endpoint**
   - Open browser or use curl:
   ```bash
   curl http://localhost:5000/api/health
   ```

   **Expected Response:**
   ```json
   {
     "status": "healthy",
     "database": "connected"
   }
   ```

---

## 🔍 Understanding the Code

### **1. Database Configuration (`app/config.py`)**

```python
# Line 95-98: Database URL from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///aeroguard.db"  # Fallback to SQLite if not set
)
```

**Explanation:**
- `os.getenv("DATABASE_URL")` reads the connection string from `.env` file
- If not found, falls back to SQLite (for local development without setup)
- This makes it easy to switch databases - just change the `.env` file!

```python
# Line 100-101: SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

**Explanation:**
- `SQLALCHEMY_DATABASE_URI`: Tells SQLAlchemy where the database is
- `SQLALCHEMY_TRACK_MODIFICATIONS = False`: Disables event system (saves memory)

```python
# Line 104-117: Connection pool settings
if DATABASE_URL.startswith("sqlite:"):
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False}
    }
else:
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,              # Max 10 connections in pool
        "pool_recycle": 3600,         # Recycle connections after 1 hour
        "pool_pre_ping": True,        # Test connection before using
        "connect_args": {"connect_timeout": 10},  # 10 sec timeout
    }
```

**Explanation:**
- **pool_size**: Maximum number of database connections to keep open
- **pool_recycle**: Prevents stale connections by recycling after 1 hour
- **pool_pre_ping**: Tests if connection is alive before using (prevents errors)
- **connect_timeout**: Fails fast if database is unreachable

---

### **2. Database Initialization (`app/database.py`)**

```python
# Line 10: Create SQLAlchemy instance
db = SQLAlchemy()
```

**Explanation:**
- Creates a global `db` object that manages all database operations
- This object is used throughout the app to define models and query data

```python
# Line 13-26: Initialize database function
def init_db(app):
    """
    Initialize database with Flask app.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)  # Connect SQLAlchemy to Flask app
    
    with app.app_context():
        try:
            db.create_all()  # Create all tables defined in models
            logger.info("✓ Database tables created successfully")
        except Exception as e:
            logger.error(f"✗ Database initialization error: {e}")
            raise
```

**Explanation:**
- `db.init_app(app)`: Links the database to your Flask application
- `app.app_context()`: Creates a context where database operations can run
- `db.create_all()`: Reads all your model classes and creates corresponding tables
  - If tables already exist, it does nothing (safe to run multiple times)
  - Creates tables based on your model definitions in `database_models.py`

---

### **3. Database Models (`app/models/database_models.py`)**

#### **User Model Example:**

```python
class User(db.Model):
    __tablename__ = 'users'  # Table name in database
    
    # Primary Key - auto-increments (1, 2, 3, ...)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Email - must be unique, cannot be null, indexed for fast lookups
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    
    # Username - must be unique, cannot be null, indexed
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Password hash - can be null (for OAuth users)
    password_hash = db.Column(db.String(255), nullable=True)
    
    # Full name - optional
    full_name = db.Column(db.String(255), nullable=True)
    
    # Account status - defaults to True
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps - automatically set
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - links to other tables
    locations = db.relationship('UserLocation', back_populates='user', cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', back_populates='user', uselist=False)
```

**Explanation:**

1. **`__tablename__ = 'users'`**
   - Specifies the actual table name in PostgreSQL
   - Without this, SQLAlchemy would use the class name

2. **Column Types:**
   - `db.Integer`: Whole numbers (1, 2, 3, ...)
   - `db.String(255)`: Text up to 255 characters
   - `db.Boolean`: True/False
   - `db.DateTime`: Date and time
   - `db.Float`: Decimal numbers

3. **Column Constraints:**
   - `primary_key=True`: Unique identifier for each row
   - `unique=True`: No two rows can have the same value
   - `nullable=False`: Must have a value (cannot be empty)
   - `index=True`: Creates an index for faster searches
   - `default=value`: Sets default value if none provided

4. **Timestamps:**
   - `default=datetime.utcnow`: Sets current time when row is created
   - `onupdate=datetime.utcnow`: Updates time whenever row is modified

5. **Relationships:**
   - `db.relationship()`: Links tables together
   - `back_populates`: Creates two-way relationship
   - `cascade='all, delete-orphan'`: When user is deleted, delete related records too
   - `uselist=False`: One-to-one relationship (not one-to-many)

#### **Foreign Key Example (AQIData):**

```python
class AQIData(db.Model):
    __tablename__ = 'aqi_data'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key - links to locations table
    location_id = db.Column(
        db.Integer, 
        db.ForeignKey('locations.id', ondelete='CASCADE'),  # Reference locations.id
        nullable=False
    )
    
    # Relationship - allows accessing location object
    location = db.relationship('Location', back_populates='aqi_data')
```

**Explanation:**
- `db.ForeignKey('locations.id')`: This column references the `id` column in `locations` table
- `ondelete='CASCADE'`: If location is deleted, delete all its AQI data too
- `location = db.relationship()`: Allows you to do `aqi_data.location.city` to get the city name

#### **Composite Index Example:**

```python
class AQIData(db.Model):
    # ... columns ...
    
    # Composite index for faster queries
    __table_args__ = (
        Index('idx_location_timestamp', 'location_id', 'timestamp'),
    )
```

**Explanation:**
- Creates an index on both `location_id` AND `timestamp` together
- Makes queries like "get all AQI data for location X between date Y and Z" very fast
- Without index: Database scans every row (slow)
- With index: Database jumps directly to relevant rows (fast)

---

### **4. Database Initialization Script (`init_db.py`)**

#### **Main Function:**

```python
@click.command()
@click.option('--drop', is_flag=True, help='Drop all tables')
@click.option('--seed', is_flag=True, help='Seed with sample data')
def main(drop, seed):
    """Database initialization utility"""
    
    # Determine environment
    env = os.getenv("FLASK_ENV", "development")
    
    # Create Flask app with appropriate config
    if env == "development":
        from app.config import DevelopmentConfig
        app = create_app(DevelopmentConfig)
    elif env == "testing":
        from app.config import TestingConfig
        app = create_app(TestingConfig)
    else:
        from app.config import ProductionConfig
        app = create_app(ProductionConfig)
    
    # Drop tables if requested
    if drop:
        drop_all_tables(app)
    
    # Initialize database
    initialize_database(app)
    
    # Seed sample data if requested
    if seed:
        seed_sample_data(app)
```

**Explanation:**
- `@click.command()`: Makes this a command-line tool
- `@click.option()`: Adds command-line flags (--drop, --seed)
- `os.getenv("FLASK_ENV")`: Reads environment from `.env` file
- `create_app(Config)`: Creates Flask app with specific configuration
- Executes functions based on flags provided

#### **Initialize Database Function:**

```python
def initialize_database(app):
    """Initialize database schema"""
    with app.app_context():
        print("\n" + "="*70)
        print("DATABASE INITIALIZATION")
        print("="*70)
        
        # Check if SQLAlchemy is already initialized
        if 'sqlalchemy' not in getattr(app, 'extensions', {}):
            init_db(app)  # Initialize if not already done
            print("✓ Database initialized via init_db")
        else:
            db.create_all()  # Just create tables
            print("✓ Database initialized (existing SQLAlchemy instance)")
```

**Explanation:**
- `app.app_context()`: Creates context needed for database operations
- Checks if SQLAlchemy is already set up (prevents double initialization)
- `db.create_all()`: Creates all tables defined in models
  - Reads all classes that inherit from `db.Model`
  - Generates CREATE TABLE SQL statements
  - Executes them in PostgreSQL
  - Skips tables that already exist

#### **Seed Sample Data Function:**

```python
def seed_sample_data(app):
    """Populate database with sample data for testing"""
    with app.app_context():
        try:
            # Create sample users
            user1 = User(
                email="alice@example.com",
                username="alice",
                full_name="Alice Johnson"
            )
            db.session.add(user1)  # Add to session (not yet in database)
            db.session.commit()     # Save to database
            
            # Create sample locations
            location = Location(
                city="Delhi",
                country="India",
                latitude=28.7041,
                longitude=77.1025,
                location_id="delhi_central"
            )
            db.session.add(location)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()  # Undo changes if error occurs
            print(f"\n✗ Error seeding data: {e}\n")
            raise
```

**Explanation:**
- `User(...)`: Creates a new user object in memory (not yet in database)
- `db.session.add()`: Stages the object to be saved
- `db.session.commit()`: Actually saves to database (executes INSERT SQL)
- `db.session.rollback()`: Undoes all changes if error occurs (keeps database consistent)

**Transaction Flow:**
```
1. Create object in Python memory
2. Add to session (staging area)
3. Commit (save to database)
   - If successful: Changes are permanent
   - If error: Rollback (undo everything)
```

---

## 🔄 Data Migration (If You Have Existing Data)

If you have existing data in NeonDB that you want to move to Supabase:

### **Option 1: Using pg_dump (Recommended)**

```bash
# 1. Export from NeonDB
pg_dump "postgresql://neondb_owner:npg_svuE7dkKTQw6@ep-odd-credit-ahje5mh1-pooler.c-3.us-east-1.aws.neon.tech/neondb" > backup.sql

# 2. Import to Supabase
psql "postgresql://postgres.xxxxx:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres" < backup.sql
```

### **Option 2: Using Python Script**

```python
# migrate_data.py
from app import create_app
from app.database import db
from app.models.database_models import *

# Connect to old database
old_app = create_app()
old_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://old-connection-string'

# Connect to new database
new_app = create_app()
new_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://new-supabase-connection-string'

# Copy data
with old_app.app_context():
    users = User.query.all()
    
with new_app.app_context():
    for user in users:
        db.session.add(user)
    db.session.commit()
```

---

## 🎨 Supabase Additional Features

Once migrated, you can leverage Supabase's extra features:

### **1. Built-in Authentication**

```python
# Instead of managing users yourself, use Supabase Auth
from supabase import create_client

supabase = create_client(
    "https://xxxxx.supabase.co",
    "your-anon-key"
)

# Sign up user
user = supabase.auth.sign_up({
    "email": "user@example.com",
    "password": "password123"
})

# Sign in
session = supabase.auth.sign_in_with_password({
    "email": "user@example.com",
    "password": "password123"
})
```

### **2. Real-time Subscriptions**

```javascript
// In your frontend
const supabase = createClient('https://xxxxx.supabase.co', 'anon-key')

// Listen for new AQI data
supabase
  .channel('aqi_updates')
  .on('postgres_changes', 
    { event: 'INSERT', schema: 'public', table: 'aqi_data' },
    (payload) => {
      console.log('New AQI data:', payload.new)
      // Update UI automatically
    }
  )
  .subscribe()
```

### **3. Auto-generated REST API**

```bash
# Supabase automatically creates REST endpoints for all tables
GET https://xxxxx.supabase.co/rest/v1/locations
GET https://xxxxx.supabase.co/rest/v1/aqi_data?location_id=eq.1
POST https://xxxxx.supabase.co/rest/v1/forecasts
```

### **4. File Storage**

```python
# Upload files (e.g., model weights, reports)
supabase.storage.from_('models').upload(
    'lstm_weights.h5',
    open('lstm_model_weights.weights.h5', 'rb')
)

# Get public URL
url = supabase.storage.from_('models').get_public_url('lstm_weights.h5')
```

---

## 🐛 Troubleshooting

### **Error: "password authentication failed"**

**Solution:** Double-check your password in the connection string. Make sure you replaced `[YOUR-PASSWORD]` with your actual password.

### **Error: "could not connect to server"**

**Solution:** 
1. Check your internet connection
2. Verify the connection string is correct
3. Make sure you're using the **Transaction** or **Session** pooler URL, not direct connection

### **Error: "relation 'users' does not exist"**

**Solution:** Run `python init_db.py` to create tables.

### **Error: "SSL connection required"**

**Solution:** Add `?sslmode=require` to the end of your connection string:
```
postgresql://postgres.xxxxx:password@host:6543/postgres?sslmode=require
```

### **Tables not showing in Supabase Dashboard**

**Solution:**
1. Refresh the page
2. Check you're looking at the correct project
3. Run `python init_db.py` again
4. Check for errors in terminal output

---

## ✅ Migration Checklist

- [ ] Created Supabase project
- [ ] Saved database password securely
- [ ] Copied connection string
- [ ] Updated `.env` file with new DATABASE_URL
- [ ] Ran `python init_db.py` successfully
- [ ] Verified tables in Supabase Dashboard
- [ ] Tested backend with `python run.py`
- [ ] Tested API endpoints
- [ ] (Optional) Migrated existing data
- [ ] (Optional) Seeded sample data with `--seed` flag
- [ ] Updated production environment variables

---

## 📚 Additional Resources

- **Supabase Documentation**: https://supabase.com/docs
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Flask-SQLAlchemy**: https://flask-sqlalchemy.palletsprojects.com/

---

## 🎉 Success!

Once you see your tables in Supabase Dashboard and your backend runs without errors, you've successfully migrated! 

Your application now benefits from:
- ✅ Reliable PostgreSQL database
- ✅ Automatic backups
- ✅ Better dashboard and monitoring
- ✅ Potential to use Supabase Auth, Storage, and Real-time features

**Need help?** Check the troubleshooting section or reach out to Supabase support!
