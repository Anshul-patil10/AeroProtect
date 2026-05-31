# 🏗️ AeroGuard Database Architecture

## 📊 Database Schema Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     AeroGuard Database Schema                    │
│                        (PostgreSQL)                              │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────────┐         ┌──────────────┐
│    users     │◄───────►│ user_preferences │         │  locations   │
│──────────────│         │──────────────────│         │──────────────│
│ id (PK)      │         │ id (PK)          │         │ id (PK)      │
│ email        │         │ user_id (FK)     │         │ location_id  │
│ username     │         │ persona          │         │ city         │
│ password_hash│         │ alert_threshold  │         │ country      │
│ full_name    │         │ forecast_hours   │         │ latitude     │
│ is_active    │         │ pollutants       │         │ longitude    │
│ created_at   │         └──────────────────┘         │ timezone     │
│ updated_at   │                                      └──────────────┘
│ last_login   │                                             │
└──────┬───────┘                                             │
       │                                                     │
       │         ┌──────────────────┐                        │
       └────────►│ user_locations   │◄───────────────────────┘
                 │──────────────────│
                 │ id (PK)          │
                 │ user_id (FK)     │
                 │ location_id (FK) │
                 │ is_favorite      │
                 │ alert_threshold  │
                 └──────────────────┘


┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  locations   │◄────────│   sensors    │         │  aqi_data    │
│──────────────│         │──────────────│◄────────│──────────────│
│ id (PK)      │         │ id (PK)      │         │ id (PK)      │
│ location_id  │         │ sensor_id    │         │ location_id  │
│ city         │         │ location_id  │         │ timestamp    │
│ country      │         │ sensor_name  │         │ pm25         │
│ latitude     │         │ latitude     │         │ pm10         │
│ longitude    │         │ longitude    │         │ aqi          │
└──────┬───────┘         │ sensor_type  │         │ temperature  │
       │                 │ provider     │         │ humidity     │
       │                 │ is_active    │         │ wind_speed   │
       │                 └──────────────┘         │ data_source  │
       │                                          └──────────────┘
       │
       │                 ┌──────────────┐
       └────────────────►│  forecasts   │
                         │──────────────│
                         │ id (PK)      │
                         │ location_id  │
                         │ forecast_time│
                         │ forecast_date│
                         │ model_type   │
                         │ horizon_hours│
                         │ aqi_forecast │
                         │ pm25_forecast│
                         │ confidence   │
                         └──────────────┘


┌──────────────────┐
│  model_metrics   │
│──────────────────│
│ id (PK)          │
│ model_type       │
│ location_id (FK) │
│ evaluation_date  │
│ mae              │
│ rmse             │
│ mape             │
│ r2_score         │
│ samples_count    │
└──────────────────┘
```

---

## 🔗 Relationships Explained

### **1. Users ↔ Locations (Many-to-Many)**

```
User "Alice" can favorite multiple locations:
  - Delhi
  - New York
  - London

Location "Delhi" can be favorited by multiple users:
  - Alice
  - Bob
  - Charlie

Junction Table: user_locations
```

**SQL Query Example:**
```sql
-- Get all locations favorited by Alice
SELECT l.city, l.country
FROM locations l
JOIN user_locations ul ON l.id = ul.location_id
JOIN users u ON u.id = ul.user_id
WHERE u.username = 'alice' AND ul.is_favorite = true;
```

**Python ORM Example:**
```python
# Get Alice's favorite locations
alice = User.query.filter_by(username='alice').first()
favorite_locations = [ul.location for ul in alice.locations if ul.is_favorite]
```

---

### **2. User ↔ UserPreference (One-to-One)**

```
Each user has exactly ONE preference record:
  User "Alice" → UserPreference (persona: health_sensitive, alert: 100)
  User "Bob"   → UserPreference (persona: general_public, alert: 150)
```

**Python ORM Example:**
```python
# Get Alice's preferences
alice = User.query.filter_by(username='alice').first()
persona = alice.preferences.persona
alert_threshold = alice.preferences.alert_threshold_aqi
```

---

### **3. Location ↔ Sensors (One-to-Many)**

```
One location can have multiple sensors:
  Location "Delhi" →
    - Sensor "Delhi Central Monitor"
    - Sensor "Delhi North Station"
    - Sensor "Delhi South Station"
```

**Python ORM Example:**
```python
# Get all sensors in Delhi
delhi = Location.query.filter_by(city='Delhi').first()
sensors = delhi.sensors
for sensor in sensors:
    print(f"{sensor.sensor_name}: {sensor.is_active}")
```

---

### **4. Location ↔ AQI Data (One-to-Many)**

```
One location has many historical AQI readings:
  Location "Delhi" →
    - AQIData (2024-01-01 00:00, pm25: 45, aqi: 120)
    - AQIData (2024-01-01 06:00, pm25: 52, aqi: 135)
    - AQIData (2024-01-01 12:00, pm25: 38, aqi: 105)
    ... (thousands of records)
```

**Python ORM Example:**
```python
# Get last 24 hours of AQI data for Delhi
from datetime import datetime, timedelta

delhi = Location.query.filter_by(city='Delhi').first()
yesterday = datetime.utcnow() - timedelta(days=1)

recent_data = AQIData.query.filter(
    AQIData.location_id == delhi.id,
    AQIData.timestamp >= yesterday
).order_by(AQIData.timestamp.desc()).all()
```

---

### **5. Location ↔ Forecasts (One-to-Many)**

```
One location has multiple forecasts (different models, times):
  Location "Delhi" →
    - Forecast (date: 2024-01-15, model: sarima, aqi: 125)
    - Forecast (date: 2024-01-15, model: xgboost, aqi: 130)
    - Forecast (date: 2024-01-15, model: ensemble, aqi: 127)
```

**Python ORM Example:**
```python
# Get today's forecasts for Delhi
from datetime import date

delhi = Location.query.filter_by(city='Delhi').first()
today = date.today()

forecasts = Forecast.query.filter(
    Forecast.location_id == delhi.id,
    Forecast.forecast_date == today
).all()

for f in forecasts:
    print(f"{f.model_type}: AQI {f.aqi_forecast} (confidence: {f.confidence})")
```

---

## 🔍 Indexes for Performance

### **Why Indexes Matter**

Without index:
```
Query: "Find AQI data for Delhi on 2024-01-15"
Database: Scans ALL rows (1,000,000 rows) → 5 seconds ❌
```

With index:
```
Query: "Find AQI data for Delhi on 2024-01-15"
Database: Jumps directly to relevant rows (100 rows) → 0.01 seconds ✅
```

### **Indexes in AeroGuard**

```python
# 1. Single Column Indexes
email = db.Column(db.String(255), index=True)  # Fast user lookup by email
city = db.Column(db.String(255), index=True)   # Fast location search by city

# 2. Composite Indexes (multiple columns together)
__table_args__ = (
    Index('idx_location_timestamp', 'location_id', 'timestamp'),
)
# Fast queries like: "Get AQI data for location X between date Y and Z"

# 3. Unique Indexes (enforces uniqueness + fast lookup)
email = db.Column(db.String(255), unique=True)  # No duplicate emails
```

---

## 🔄 Cascade Delete Behavior

### **What is CASCADE?**

When you delete a parent record, what happens to child records?

```python
location_id = db.Column(
    db.Integer, 
    db.ForeignKey('locations.id', ondelete='CASCADE')
)
```

**Example:**
```
Delete Location "Delhi"
  ↓ CASCADE
  → Deletes all sensors in Delhi
  → Deletes all AQI data for Delhi
  → Deletes all forecasts for Delhi
  → Removes Delhi from user favorites
```

**Without CASCADE:**
```
Delete Location "Delhi"
  ↓ ERROR
  ✗ Cannot delete: sensors still reference this location
```

### **Cascade Options:**

| Option | Behavior |
|--------|----------|
| `CASCADE` | Delete child records automatically |
| `SET NULL` | Set foreign key to NULL in child records |
| `RESTRICT` | Prevent deletion if children exist |
| `NO ACTION` | Same as RESTRICT (default) |

---

## 📈 Data Flow Example

### **Scenario: User Checks AQI for Delhi**

```
1. Frontend Request
   GET /api/aqi/realtime?city=Delhi

2. Backend Route (realtime_aqi.py)
   @app.route('/api/aqi/realtime')
   def get_realtime_aqi():
       city = request.args.get('city')
       
3. Database Query
   location = Location.query.filter_by(city=city).first()
   latest_aqi = AQIData.query.filter_by(
       location_id=location.id
   ).order_by(AQIData.timestamp.desc()).first()
   
4. SQL Generated by SQLAlchemy
   SELECT * FROM locations WHERE city = 'Delhi' LIMIT 1;
   SELECT * FROM aqi_data 
   WHERE location_id = 123 
   ORDER BY timestamp DESC 
   LIMIT 1;
   
5. PostgreSQL Execution
   - Uses index on 'city' column → Fast lookup
   - Uses index on 'location_id' + 'timestamp' → Fast sorting
   - Returns result in ~10ms
   
6. Backend Response
   {
     "city": "Delhi",
     "aqi": 125,
     "pm25": 45.2,
     "timestamp": "2024-01-15T10:30:00Z"
   }
```

---

## 🎯 Query Optimization Tips

### **1. Use Indexes**
```python
# BAD: No index
city = db.Column(db.String(255))  # Slow searches

# GOOD: With index
city = db.Column(db.String(255), index=True)  # Fast searches
```

### **2. Limit Results**
```python
# BAD: Load all data (millions of rows)
all_data = AQIData.query.all()  # Memory overflow!

# GOOD: Limit and paginate
recent_data = AQIData.query.limit(100).all()
```

### **3. Use Joins Instead of Multiple Queries**
```python
# BAD: N+1 query problem
locations = Location.query.all()
for loc in locations:
    sensors = Sensor.query.filter_by(location_id=loc.id).all()  # Query per location!

# GOOD: Single query with join
locations = Location.query.options(
    db.joinedload(Location.sensors)
).all()
```

### **4. Select Only Needed Columns**
```python
# BAD: Load all columns
users = User.query.all()  # Loads password_hash, etc.

# GOOD: Select specific columns
usernames = db.session.query(User.username, User.email).all()
```

---

## 🔐 Security Best Practices

### **1. Never Store Plain Passwords**
```python
# BAD
user.password = "mypassword123"  # Plain text!

# GOOD
from werkzeug.security import generate_password_hash
user.password_hash = generate_password_hash("mypassword123")
```

### **2. Use Parameterized Queries**
```python
# BAD: SQL Injection vulnerability
city = request.args.get('city')
query = f"SELECT * FROM locations WHERE city = '{city}'"  # Dangerous!

# GOOD: SQLAlchemy handles this automatically
location = Location.query.filter_by(city=city).first()  # Safe
```

### **3. Validate Input**
```python
# BAD: No validation
aqi = request.json.get('aqi')
aqi_data = AQIData(aqi=aqi)  # Could be negative, string, etc.

# GOOD: Validate
aqi = request.json.get('aqi')
if not isinstance(aqi, (int, float)) or aqi < 0 or aqi > 500:
    return {"error": "Invalid AQI value"}, 400
aqi_data = AQIData(aqi=aqi)
```

---

## 📊 Database Size Estimates

### **Expected Data Volume**

| Table | Rows per Location | Total (10 locations) | Size |
|-------|-------------------|----------------------|------|
| locations | 1 | 10 | 1 KB |
| sensors | 3 | 30 | 5 KB |
| aqi_data | 8,760/year (hourly) | 87,600/year | ~10 MB/year |
| forecasts | 90/day (3 models × 30 days) | 900/day | ~1 MB/month |
| users | - | 1,000 | 100 KB |
| user_preferences | - | 1,000 | 50 KB |
| user_locations | 5 per user | 5,000 | 200 KB |
| model_metrics | 30/month | 300/month | 50 KB/month |

**Total for 1 year:** ~120 MB (well within free tier limits)

---

## 🎉 Summary

Your database architecture is:
- ✅ **Normalized**: No data duplication
- ✅ **Indexed**: Fast queries
- ✅ **Relational**: Proper foreign keys and relationships
- ✅ **Scalable**: Can handle millions of records
- ✅ **Secure**: Password hashing, parameterized queries
- ✅ **Maintainable**: Clear structure and naming

**Migration to Supabase is just changing the connection string!** 🚀
