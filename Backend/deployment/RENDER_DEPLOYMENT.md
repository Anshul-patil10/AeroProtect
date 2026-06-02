# AeroGuard Backend - Render Deployment Guide

## 📋 Two Deployment Methods

### Method 1: Using render.yaml (Recommended - Infrastructure as Code)
✅ Automated configuration
✅ Version controlled
✅ Easy to replicate
✅ Best practice

### Method 2: Manual Dashboard Configuration
✅ More control
✅ Good for learning
✅ Easier to troubleshoot

---

## 🚀 Method 1: Deploy with render.yaml (Recommended)

### Step 1: Push Code to GitHub

**Files included:**
- ✅ `render.yaml` - Render configuration (Infrastructure as Code)
- ✅ `runtime.txt` - Python 3.11.9
- ✅ `requirements-fixed.txt` - Dependencies

```bash
git add .
git commit -m "Add Render configuration for deployment"
git push origin main
```

### Step 2: Connect to Render

1. Go to [render.com](https://render.com) and login
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select **AeroGuard** repository
5. Render will detect `render.yaml` automatically

### Step 3: Set Secret Environment Variables

Render will prompt you to set these (marked as `sync: false` in render.yaml):

```bash
DATABASE_URL=<your-supabase-connection-string>
GEMINI_API_KEY=<your-gemini-api-key>
REALTIME_WAQI_API_KEY=<your-waqi-api-key>
```

**Generate Secret Keys (if needed):**
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32)); print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

### Step 4: Deploy

1. Click **"Apply"**
2. Render will:
   - Read `render.yaml`
   - Create the web service
   - Install dependencies
   - Start your app
3. Wait 3-5 minutes

### Step 5: Update CORS

After deployment, update `CORS_ORIGINS` in Render dashboard:
```
CORS_ORIGINS=https://your-frontend.vercel.app,https://aeroguard-backend.onrender.com
```

---

## 🚀 Method 2: Manual Dashboard Configuration

## 🚀 Quick Deployment Checklist

### Step 1: Push Code to GitHub

**Important Files Created:**
- ✅ `runtime.txt` - Specifies Python 3.11.9 (compatible with all dependencies)
- ✅ `requirements-fixed.txt` - Updated pandas version for compatibility

```bash
git add .
git commit -m "Prepare for Render deployment with Python 3.11"
git push origin main
```

### Step 2: Create Render Web Service
1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Select **AeroGuard** repository

### Step 3: Configure Service Settings

| Setting | Value |
|---------|-------|
| **Name** | `aeroguard-backend` |
| **Region** | Singapore (or closest to you) |
| **Branch** | `main` |
| **Root Directory** | `Backend` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements-fixed.txt` |
| **Start Command** | `gunicorn --bind 0.0.0.0:$PORT wsgi:app` |

### Step 4: Environment Variables

Copy these into Render's Environment tab:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=<generate-using-python-secrets>
JWT_SECRET_KEY=<generate-using-python-secrets>

# Database (Supabase)
DATABASE_URL=<your-supabase-connection-string>

# CORS (Update with your actual frontend URL after deployment)
CORS_ORIGINS=<your-frontend-url>,*

# API Keys
GEMINI_API_KEY=<your-gemini-api-key>
GEMINI_MODEL=gemini-pro
REALTIME_WAQI_API_KEY=<your-waqi-api-key>
REALTIME_WAQI_BASE_URL=https://api.waqi.info

# Model Settings
MODEL_DIR=models/saved
MODEL_CACHE_TIMEOUT=3600
MAX_FORECAST_DAYS=30
MIN_FORECAST_DAYS=1
DEFAULT_FORECAST_DAYS=7

# Request Settings
MAX_REQUEST_SIZE=1048576
REQUEST_TIMEOUT=30
LOG_LEVEL=INFO
```

**Generate Secret Keys:**
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32)); print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

### Step 5: Deploy
1. Click **"Create Web Service"**
2. Wait 2-5 minutes for deployment
3. You'll get a URL like: `https://aeroguard-backend.onrender.com`

### Step 6: Test Deployment

Test these endpoints in your browser or Postman:

```bash
# Health check
https://aeroguard-backend.onrender.com/health

# Root endpoint
https://aeroguard-backend.onrender.com/

# API health
https://aeroguard-backend.onrender.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-31T...",
  "version": "1.0.0",
  "service": "AeroGuard"
}
```

### Step 7: Initialize Database (Optional)

If you need to run database initialization:

1. Go to Render Dashboard → Your Service → **Shell** tab
2. Run:
```bash
python init_db.py
```

---

## 🔧 Troubleshooting

### Build Fails with Pandas/Cython Error ⭐ FIXED
**Problem:** `error: metadata-generation-failed` for pandas
**Cause:** Render using Python 3.14 (too new for pandas)
**Solution:** ✅ Already fixed with THREE methods:
- `.python-version` file (3.11.9) - Most reliable
- `runtime.txt` file (python-3.11.9) - Backup
- `render.yaml` runtimeVersion - Triple redundancy

**If still failing:**
1. Clear build cache in Render dashboard
2. Manual Deploy → "Clear build cache & deploy"
3. Check logs for: `==> Using Python version 3.11.9`

See detailed fix: [`PYTHON_VERSION_FIX.md`](../PYTHON_VERSION_FIX.md)

### Build Fails
- Check logs in Render dashboard
- Verify `requirements-fixed.txt` has all dependencies
- Ensure Python version compatibility

### App Crashes on Start
- Check environment variables are set correctly
- Verify DATABASE_URL is correct
- Check logs for specific errors

### Database Connection Issues
- Verify Supabase database is running
- Check DATABASE_URL format
- Ensure Supabase allows connections from Render IPs

### CORS Errors
- Update CORS_ORIGINS with your frontend URL
- Redeploy after changing environment variables

---

## 📝 Post-Deployment Tasks

1. **Update Frontend**: Change API base URL to your Render URL
2. **Monitor Logs**: Check Render dashboard for any errors
3. **Test All Endpoints**: Verify forecast, health risk, analytics work
4. **Update CORS**: Add your production frontend URL

---

## 💡 Important Notes

### Free Tier Limitations
- ⚠️ Service spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes 30-60 seconds (cold start)
- ⚠️ 750 hours/month free

### Recommendations
- Consider paid plan ($7/month) to avoid cold starts
- Use health check pings to keep service warm
- Monitor usage in Render dashboard

---

## 🎯 Your Deployment URLs

After deployment, save these:

- **Backend URL**: `https://aeroguard-backend.onrender.com`
- **Health Check**: `https://aeroguard-backend.onrender.com/health`
- **API Base**: `https://aeroguard-backend.onrender.com/api/v1`

Update your frontend's API configuration with the Backend URL!

---

## ✅ Deployment Complete!

Your backend is now live on Render. Next steps:
1. Test all endpoints
2. Update frontend to use new backend URL
3. Deploy frontend on Vercel
4. Celebrate! 🎉
