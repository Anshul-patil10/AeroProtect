# AeroGuard Backend API

Air Quality Forecasting System with Machine Learning - Backend API built with Flask.

## 📁 Project Structure

```
Backend/
├── app/                          # Main application package
│   ├── models/                   # ML models & database models
│   ├── routes/                   # API endpoints
│   ├── services/                 # Business logic
│   ├── utils/                    # Utilities & helpers
│   ├── __init__.py              # App factory
│   ├── config.py                # Configuration
│   └── database.py              # Database setup
├── deployment/                   # Deployment configurations
│   ├── docker-compose.yml       # Docker setup
│   ├── Dockerfile               # Docker image
│   └── RENDER_DEPLOYMENT.md     # Render deployment guide
├── docs/                        # Documentation
│   ├── DATABASE_ARCHITECTURE.md # Database schema
│   ├── SUPABASE_MIGRATION_GUIDE.md
│   └── ...                      # Other docs
├── instance/                    # SQLite database (local dev)
├── scripts/                     # Utility scripts
├── tests/                       # Test files
│   ├── test_connection.py
│   ├── check_tables.py
│   └── ...
├── .env                         # Environment variables (not in git)
├── .gitignore                   # Git ignore rules
├── init_db.py                   # Database initialization
├── init_db_simple.py            # Simple DB init
├── requirements-fixed.txt       # Python dependencies
├── run.py                       # Development server
├── runtime.txt                  # Python version (for Render)
└── wsgi.py                      # Production WSGI entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (Supabase recommended)
- pip

### 1. Clone & Setup
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-fixed.txt
```

### 2. Configure Environment
Create `.env` file:
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/database

# Flask
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# API Keys
GEMINI_API_KEY=your-gemini-key
REALTIME_WAQI_API_KEY=your-waqi-key
```

### 3. Initialize Database
```bash
python init_db.py
```

### 4. Run Development Server
```bash
python run.py
```

Server runs at: `http://localhost:5000`

## 📡 API Endpoints

### Health & Info
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/v1/health` - API health check

### Core Features
- `POST /api/v1/forecast` - Air quality forecast
- `GET /api/v1/realtime-aqi` - Real-time AQI data
- `POST /api/v1/health-risk` - Health risk assessment
- `GET /api/v1/historical-analysis` - Historical data analysis
- `POST /api/v1/generative-ai/explain` - AI explanations
- `GET /api/v1/analytics` - Analytics data

### User Management
- `POST /api/v1/users/register` - Register user
- `POST /api/v1/users/login` - Login user
- `GET /api/v1/users/profile` - Get profile

## 🧪 Testing

Run tests:
```bash
# Test database connection
python tests/test_connection.py

# Check tables
python tests/check_tables.py

# Verify data
python tests/verify_supabase_data.py
```

## 🚢 Deployment

### Render (Recommended)
See detailed guide: [`deployment/RENDER_DEPLOYMENT.md`](deployment/RENDER_DEPLOYMENT.md)

**Quick Deploy:**
1. Push to GitHub
2. Connect to Render
3. Set environment variables
4. Deploy!

### Docker
```bash
cd deployment
docker-compose up -d
```

## 📚 Documentation

- **Database**: [`docs/DATABASE_ARCHITECTURE.md`](docs/DATABASE_ARCHITECTURE.md)
- **Migration**: [`docs/SUPABASE_MIGRATION_GUIDE.md`](docs/SUPABASE_MIGRATION_GUIDE.md)
- **Deployment**: [`deployment/RENDER_DEPLOYMENT.md`](deployment/RENDER_DEPLOYMENT.md)
- **Security**: [`docs/SECURITY_CLEANUP.md`](docs/SECURITY_CLEANUP.md)

## 🛠️ Tech Stack

- **Framework**: Flask 3.0
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy
- **ML**: TensorFlow, XGBoost, SARIMA
- **API**: RESTful
- **Auth**: JWT
- **Server**: Gunicorn

## 🔐 Security

- JWT authentication
- CORS protection
- Environment variables for secrets
- SQL injection prevention (SQLAlchemy)
- Input validation

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `SECRET_KEY` | Flask secret key | ✅ |
| `JWT_SECRET_KEY` | JWT signing key | ✅ |
| `GEMINI_API_KEY` | Google Gemini API key | ✅ |
| `REALTIME_WAQI_API_KEY` | WAQI API key | ✅ |
| `FLASK_ENV` | Environment (development/production) | ❌ |
| `CORS_ORIGINS` | Allowed CORS origins | ❌ |

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

MIT License

## 🆘 Support

- Check [`docs/`](docs/) for detailed documentation
- Review [`tests/`](tests/) for examples
- See [`deployment/`](deployment/) for deployment guides

---

**Built with ❤️ for cleaner air**
