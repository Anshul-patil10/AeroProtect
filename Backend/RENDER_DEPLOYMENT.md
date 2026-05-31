# AeroGuard Backend - Render Deployment Guide

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
SECRET_KEY=61ab5fc5e417e398777e6a50e68ba36ca70aad81606b31641282b14f3247dbfd
JWT_SECRET_KEY=4d4ed571c102524901fe5dbbae55ef59bc5b92dc257730b8c49698fe8c56f795

# Database (Supabase)
DATABASE_URL=postgresql://postgres.nnsnqmxyullfgnsijtns:AeroProtect.2026@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres

# CORS (Update with your actual frontend URL after deployment)
CORS_ORIGINS=https://aero-guard-deploy.vercel.app,*

# API Keys
GEMINI_API_KEY=AIzaSyBXrw9AWAyWooRWAy9sTWN2sKakVrIg1Ko
GEMINI_MODEL=gemini-pro
REALTIME_WAQI_API_KEY=ce447e42616daf4acaa532f376215a74eab11403
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

### Build Fails with Pandas/Cython Error
**Problem:** `error: metadata-generation-failed` for pandas
**Solution:** ✅ Already fixed! We created `runtime.txt` to use Python 3.11.9
- Render was using Python 3.14 (too new for pandas 2.2.0)
- `runtime.txt` forces Python 3.11.9 (stable and compatible)

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
