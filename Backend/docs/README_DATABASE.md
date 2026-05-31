# 📚 AeroGuard Database Documentation

## 🎯 Quick Start

**Important Discovery:** Your application is **already using PostgreSQL** (NeonDB), not MongoDB! This means migrating to Supabase is extremely simple - just change the connection string.

---

## 📖 Documentation Files

This directory contains comprehensive documentation about your database setup and migration:

### **1. 🚀 Quick Migration (Start Here!)**
**File:** `QUICK_MIGRATION_STEPS.md`

5-minute guide to migrate from NeonDB to Supabase. Perfect if you just want to get it done quickly.

**What you'll learn:**
- How to create a Supabase project
- How to get your connection string
- How to update your `.env` file
- How to initialize the database

---

### **2. 📘 Complete Migration Guide**
**File:** `SUPABASE_MIGRATION_GUIDE.md`

Comprehensive guide with detailed explanations of every step and every line of code.

**What you'll learn:**
- Why migrate to Supabase
- Step-by-step migration process
- Detailed code explanations
- How to migrate existing data
- Supabase additional features
- Troubleshooting common issues

**Sections:**
- Overview
- Step-by-step migration (with screenshots)
- Understanding the code (line-by-line)
- Data migration options
- Supabase bonus features
- Troubleshooting
- Success checklist

---

### **3. 🏗️ Database Architecture**
**File:** `DATABASE_ARCHITECTURE.md`

Visual diagrams and explanations of your database structure.

**What you'll learn:**
- Database schema overview
- Table relationships explained
- How indexes work
- Query optimization tips
- Security best practices
- Data flow examples

**Includes:**
- ASCII diagrams of table relationships
- SQL and Python ORM examples
- Performance optimization tips
- Security guidelines

---

### **4. ⚖️ NeonDB vs Supabase Comparison**
**File:** `NEONDB_VS_SUPABASE.md`

Detailed comparison to help you decide which database to use.

**What you'll learn:**
- Feature-by-feature comparison
- Pricing comparison
- Performance differences
- When to use each
- Migration effort

**Comparison areas:**
- Database performance
- Developer experience
- Built-in features
- Authentication
- Real-time updates
- File storage
- Auto-generated APIs

---

## 🗂️ Database Files

### **Configuration Files**

```
Backend/
├── .env                          # Environment variables (DATABASE_URL here!)
├── app/
│   ├── config.py                 # Application configuration
│   ├── database.py               # Database initialization
│   └── models/
│       └── database_models.py    # SQLAlchemy ORM models
└── init_db.py                    # Database initialization script
```

### **Key Files Explained**

#### **`.env`**
Contains your database connection string and other environment variables.

```env
DATABASE_URL=postgresql://user:password@host:5432/database
```

#### **`app/config.py`**
Application configuration for different environments (development, testing, production).

**Key settings:**
- Database connection pooling
- CORS origins
- API keys
- Logging levels

#### **`app/database.py`**
Initializes SQLAlchemy with Flask and creates database tables.

**Key functions:**
- `init_db(app)`: Initialize database with Flask app
- `get_db()`: Get current database session

#### **`app/models/database_models.py`**
Defines all database tables using SQLAlchemy ORM.

**Models:**
- `User`: User accounts
- `UserPreference`: User settings
- `Location`: Geographic locations
- `Sensor`: Air quality sensors
- `AQIData`: Historical measurements
- `Forecast`: Predicted values
- `UserLocation`: User-location relationships
- `ModelMetrics`: ML model performance

#### **`init_db.py`**
Command-line tool to initialize and seed the database.

**Usage:**
```bash
python init_db.py              # Create tables
python init_db.py --drop       # Drop all tables (careful!)
python init_db.py --seed       # Add sample data
```

---

## 🚀 Common Tasks

### **Initialize Database**
```bash
cd "d:\VS-Code projects\AeroGuard_\Backend"
python init_db.py
```

### **Add Sample Data**
```bash
python init_db.py --seed
```

### **Reset Database**
```bash
python init_db.py --drop
python init_db.py --seed
```

### **Run Backend**
```bash
python run.py
```

### **Test Database Connection**
```bash
curl http://localhost:5000/api/health
```

---

## 🔍 Database Schema Summary

### **Tables**

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `users` | User accounts | email, username, password_hash |
| `user_preferences` | User settings | persona, alert_threshold |
| `locations` | Geographic locations | city, country, lat, lng |
| `sensors` | Air quality sensors | sensor_id, location_id |
| `aqi_data` | Historical measurements | timestamp, pm25, aqi |
| `forecasts` | Predicted values | forecast_date, model_type |
| `user_locations` | User favorites | user_id, location_id |
| `model_metrics` | ML performance | mae, rmse, r2_score |

### **Relationships**

```
users ←→ user_preferences (one-to-one)
users ←→ locations (many-to-many via user_locations)
locations ←→ sensors (one-to-many)
locations ←→ aqi_data (one-to-many)
locations ←→ forecasts (one-to-many)
```

---

## 🎓 Learning Path

### **Beginner: Just Want to Migrate**
1. Read `QUICK_MIGRATION_STEPS.md`
2. Follow the 5 steps
3. Done! ✅

### **Intermediate: Want to Understand**
1. Read `QUICK_MIGRATION_STEPS.md`
2. Read `SUPABASE_MIGRATION_GUIDE.md` (Understanding the Code section)
3. Read `DATABASE_ARCHITECTURE.md` (Schema Overview)

### **Advanced: Want to Master**
1. Read all documentation files
2. Study `database_models.py` code
3. Read `DATABASE_ARCHITECTURE.md` (Query Optimization)
4. Read `NEONDB_VS_SUPABASE.md` (Feature Comparison)

---

## 🆘 Troubleshooting

### **Can't connect to database**
1. Check `.env` file has correct `DATABASE_URL`
2. Verify password is correct
3. Test internet connection
4. Check Supabase project is active

### **Tables not created**
1. Run `python init_db.py`
2. Check terminal for error messages
3. Verify database connection works

### **Import errors**
1. Activate virtual environment
2. Install dependencies: `pip install -r requirements-fixed.txt`
3. Check Python version (3.8+)

### **Need more help?**
- Check `SUPABASE_MIGRATION_GUIDE.md` → Troubleshooting section
- Check Supabase documentation: https://supabase.com/docs
- Check SQLAlchemy documentation: https://docs.sqlalchemy.org/

---

## 📊 Current Setup

### **Database Provider**
- **Current:** NeonDB (PostgreSQL)
- **Alternative:** Supabase (PostgreSQL)
- **Migration:** 5 minutes (just change connection string!)

### **ORM**
- **Library:** SQLAlchemy 2.0.25
- **Integration:** Flask-SQLAlchemy 3.1.1
- **Driver:** psycopg2-binary 2.9.9

### **Connection**
- **Pooling:** Enabled (10 connections)
- **SSL:** Required
- **Timeout:** 10 seconds

---

## 🎯 Next Steps

### **Option 1: Keep NeonDB**
Your current setup works perfectly! No action needed.

**Advantages:**
- ✅ Already configured
- ✅ Auto-scaling
- ✅ Database branching
- ✅ 10 free projects

### **Option 2: Migrate to Supabase**
Get additional features beyond just database.

**Advantages:**
- ✅ Built-in authentication
- ✅ Real-time subscriptions
- ✅ File storage
- ✅ Auto-generated APIs
- ✅ Better dashboard

**How to migrate:**
1. Read `QUICK_MIGRATION_STEPS.md`
2. Follow 5 simple steps
3. Done in 5 minutes!

---

## 📚 Additional Resources

### **Official Documentation**
- **Supabase:** https://supabase.com/docs
- **NeonDB:** https://neon.tech/docs
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **Flask-SQLAlchemy:** https://flask-sqlalchemy.palletsprojects.com/
- **PostgreSQL:** https://www.postgresql.org/docs/

### **Tutorials**
- **SQLAlchemy ORM Tutorial:** https://docs.sqlalchemy.org/en/20/tutorial/
- **Supabase Python Client:** https://supabase.com/docs/reference/python/
- **PostgreSQL Tutorial:** https://www.postgresqltutorial.com/

### **Tools**
- **pgAdmin:** PostgreSQL GUI client
- **DBeaver:** Universal database tool
- **Supabase Studio:** Built-in web interface

---

## ✅ Checklist

### **Database Setup**
- [x] Database models created (`database_models.py`)
- [x] Configuration files set up (`.env`, `config.py`)
- [x] Initialization script ready (`init_db.py`)
- [ ] Database initialized (run `python init_db.py`)
- [ ] Sample data seeded (optional: `python init_db.py --seed`)

### **Migration (if choosing Supabase)**
- [ ] Supabase project created
- [ ] Connection string obtained
- [ ] `.env` file updated
- [ ] Database initialized
- [ ] Backend tested
- [ ] Tables verified in dashboard

### **Documentation**
- [x] Quick migration guide created
- [x] Complete migration guide created
- [x] Architecture documentation created
- [x] Comparison guide created
- [x] README created

---

## 🎉 You're All Set!

Your database is ready to use. Choose your path:

1. **Quick Migration:** Read `QUICK_MIGRATION_STEPS.md`
2. **Detailed Guide:** Read `SUPABASE_MIGRATION_GUIDE.md`
3. **Understand Architecture:** Read `DATABASE_ARCHITECTURE.md`
4. **Compare Options:** Read `NEONDB_VS_SUPABASE.md`

**Questions?** All documentation files have detailed explanations and troubleshooting sections.

**Happy coding! 🚀**
