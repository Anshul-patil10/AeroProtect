# 📁 AeroGuard Backend - Project Structure

## Clean & Organized Structure

```
Backend/
│
├── 📱 app/                          # Main Application Package
│   ├── models/                      # ML models & database models
│   │   ├── database_models.py       # SQLAlchemy models
│   │   ├── forecast_model.py        # Forecasting logic
│   │   ├── lstm_model.py            # LSTM neural network
│   │   ├── sarima_model.py          # SARIMA time series
│   │   └── xgboost_model.py         # XGBoost model
│   │
│   ├── routes/                      # API Endpoints (Blueprints)
│   │   ├── health.py                # Health checks
│   │   ├── forecast.py              # Forecast endpoints
│   │   ├── realtime_aqi.py          # Real-time AQI
│   │   ├── health_risk.py           # Health risk assessment
│   │   ├── historical_analysis.py   # Historical data
│   │   ├── generative_ai.py         # AI explanations
│   │   ├── analytics_route.py       # Analytics
│   │   ├── user.py                  # User management
│   │   └── model_comparison.py      # Model comparison
│   │
│   ├── services/                    # Business Logic Layer
│   │   ├── forecasting_service.py   # Forecast logic
│   │   ├── health_risk.py           # Health calculations
│   │   ├── realtime_aqi_service.py  # AQI data fetching
│   │   ├── analytics_service.py     # Analytics logic
│   │   ├── data_preprocessing.py    # Data cleaning
│   │   └── generative_explainer.py  # AI explanations
│   │
│   ├── utils/                       # Utilities & Helpers
│   │   ├── constants.py             # App constants
│   │   ├── error_handlers.py        # Error handling
│   │   ├── validators.py            # Input validation
│   │   ├── preprocessors.py         # Data preprocessing
│   │   └── startup.py               # Startup checks
│   │
│   ├── __init__.py                  # App Factory
│   ├── config.py                    # Configuration classes
│   └── database.py                  # Database initialization
│
├── 🚀 deployment/                   # Deployment Configurations
│   ├── docker-compose.yml           # Docker setup
│   ├── Dockerfile                   # Docker image
│   ├── RENDER_DEPLOYMENT.md         # Render guide (detailed)
│   ├── DEPLOYMENT_METHODS.md        # Method comparison
│   └── QUICK_START.md               # 5-minute deploy guide
│
├── 📚 docs/                         # Documentation
│   ├── DATABASE_ARCHITECTURE.md     # Database schema
│   ├── SUPABASE_MIGRATION_GUIDE.md  # Migration guide
│   ├── NEONDB_VS_SUPABASE.md        # DB comparison
│   ├── QUICK_MIGRATION_STEPS.md     # Quick migration
│   ├── README_DATABASE.md           # Database docs
│   ├── MIGRATION_SUMMARY.txt        # Migration summary
│   └── SECURITY_CLEANUP.md          # Security notes
│
├── 🧪 tests/                        # Test Files
│   ├── test_connection.py           # DB connection test
│   ├── check_connection.py          # Connection checker
│   ├── check_tables.py              # Table verification
│   ├── test_add_data.py             # Data insertion test
│   ├── verify_supabase_tables.py    # Supabase tables
│   └── verify_supabase_data.py      # Supabase data
│
├── 💾 instance/                     # SQLite Database (Local Dev)
│   └── aeroguard.db                 # Local database file
│
├── 🛠️ scripts/                      # Utility Scripts
│   └── verify_cors.py               # CORS verification
│
├── 📄 Root Files                    # Configuration & Entry Points
│   ├── .env                         # Environment variables (SECRET!)
│   ├── .gitignore                   # Git ignore rules
│   ├── render.yaml                  # Render config (IaC) ⭐ NEW
│   ├── runtime.txt                  # Python version ⭐ NEW
│   ├── requirements-fixed.txt       # Python dependencies
│   ├── init_db.py                   # Database initialization
│   ├── init_db_simple.py            # Simple DB init
│   ├── run.py                       # Development server
│   ├── wsgi.py                      # Production entry point
│   ├── README.md                    # Main documentation ⭐ NEW
│   └── PROJECT_STRUCTURE.md         # This file ⭐ NEW
│
└── 🗑️ .do/                          # DigitalOcean config (legacy)
```

---

## 📂 Folder Purposes

### `/app` - Main Application
**Purpose:** Core application code
**Contains:** Models, routes, services, utilities
**Why:** Organized by function (MVC-like pattern)

### `/deployment` - Deployment Files
**Purpose:** Everything needed to deploy
**Contains:** Docker, Render configs, deployment guides
**Why:** Separate deployment from application code

### `/docs` - Documentation
**Purpose:** All documentation in one place
**Contains:** Database docs, migration guides, architecture
**Why:** Easy to find and maintain documentation

### `/tests` - Test Files
**Purpose:** Testing and verification scripts
**Contains:** Connection tests, data verification
**Why:** Keep tests separate from application code

### `/instance` - Local Database
**Purpose:** SQLite database for local development
**Contains:** Local database file
**Why:** Auto-generated by Flask-SQLAlchemy

### `/scripts` - Utility Scripts
**Purpose:** Helper scripts for maintenance
**Contains:** CORS verification, data scripts
**Why:** Separate utilities from core app

---

## 🎯 Key Files Explained

### Configuration Files
| File | Purpose |
|------|---------|
| `render.yaml` | Render deployment config (Infrastructure as Code) |
| `runtime.txt` | Specifies Python 3.11.9 for Render |
| `requirements-fixed.txt` | Python dependencies |
| `.env` | Environment variables (NOT in git) |
| `.gitignore` | Files to exclude from git |

### Entry Points
| File | Purpose |
|------|---------|
| `run.py` | Development server (Flask dev server) |
| `wsgi.py` | Production server (Gunicorn entry point) |

### Database
| File | Purpose |
|------|---------|
| `init_db.py` | Initialize database with tables |
| `init_db_simple.py` | Simple database initialization |
| `app/database.py` | Database configuration |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `PROJECT_STRUCTURE.md` | This file - structure explanation |
| `deployment/QUICK_START.md` | 5-minute deployment guide |
| `deployment/RENDER_DEPLOYMENT.md` | Detailed deployment guide |

---

## 🆕 What Changed?

### Before (Messy)
```
Backend/
├── app/
├── test_connection.py
├── check_tables.py
├── DATABASE_ARCHITECTURE.md
├── RENDER_DEPLOYMENT.md
├── docker-compose.yml
├── Dockerfile
└── ... (20+ files in root)
```

### After (Clean) ✅
```
Backend/
├── app/                    # Application code
├── deployment/             # Deployment files
├── docs/                   # Documentation
├── tests/                  # Test files
├── render.yaml            # Render config
├── README.md              # Main docs
└── ... (only 8 files in root)
```

---

## 📝 Benefits of New Structure

### ✅ Organized
- Similar files grouped together
- Easy to find what you need
- Clear separation of concerns

### ✅ Professional
- Industry-standard structure
- Easy for new developers to understand
- Follows best practices

### ✅ Maintainable
- Documentation in one place
- Tests separate from code
- Deployment configs isolated

### ✅ Scalable
- Easy to add new features
- Clear where new files go
- Room for growth

---

## 🚀 Quick Navigation

**Want to:**
- **Deploy?** → `deployment/QUICK_START.md`
- **Understand database?** → `docs/DATABASE_ARCHITECTURE.md`
- **Run tests?** → `tests/`
- **Configure app?** → `.env` and `app/config.py`
- **Add API endpoint?** → `app/routes/`
- **Add business logic?** → `app/services/`

---

## 🎓 Learning Path

1. **Start here:** `README.md` - Overview
2. **Understand structure:** `PROJECT_STRUCTURE.md` (this file)
3. **Setup locally:** Follow README Quick Start
4. **Deploy:** `deployment/QUICK_START.md`
5. **Deep dive:** Explore `docs/` folder

---

**Structure is clean, organized, and ready for production! 🎉**
