# 🚀 Quick Start - Deploy to Render in 5 Minutes

## Prerequisites
- ✅ Code pushed to GitHub
- ✅ Render account created
- ✅ Supabase database ready

---

## Option A: Deploy with render.yaml (Recommended)

### 1. Push Code
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Blueprint"**
3. Select your repository
4. Render detects `render.yaml` ✅

### 3. Set Secrets
Add these in Render dashboard:
```
DATABASE_URL=<your-supabase-url>
GEMINI_API_KEY=<your-key>
REALTIME_WAQI_API_KEY=<your-key>
```

### 4. Deploy
Click **"Apply"** → Wait 3-5 minutes → Done! 🎉

---

## Option B: Manual Dashboard Setup

### 1. Create Web Service
- Go to Render → "New +" → "Web Service"
- Connect repository

### 2. Configure
```
Name: aeroguard-backend
Runtime: Python 3
Branch: main
Root Directory: Backend
Build Command: pip install -r requirements-fixed.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

### 3. Add Environment Variables
Copy from `deployment/RENDER_DEPLOYMENT.md`

### 4. Deploy
Click "Create Web Service" → Wait 3-5 minutes → Done! 🎉

---

## Test Your Deployment

Visit these URLs (replace with your Render URL):

```
https://aeroguard-backend.onrender.com/health
https://aeroguard-backend.onrender.com/
https://aeroguard-backend.onrender.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-31T...",
  "service": "AeroGuard"
}
```

---

## Next Steps

1. ✅ Backend deployed
2. ⏳ Update frontend API URL
3. ⏳ Test all endpoints
4. ⏳ Deploy frontend to Vercel

---

## Troubleshooting

**Build fails?**
- Check logs in Render dashboard
- Verify `runtime.txt` exists (Python 3.11.9)
- Check `requirements-fixed.txt`

**App crashes?**
- Verify DATABASE_URL is correct
- Check all environment variables are set
- Review logs for errors

**Can't connect?**
- Check Supabase database is running
- Verify CORS_ORIGINS includes your frontend URL

---

## Files Reference

- `render.yaml` - Deployment configuration
- `runtime.txt` - Python version
- `requirements-fixed.txt` - Dependencies
- `wsgi.py` - Production entry point
- `deployment/RENDER_DEPLOYMENT.md` - Detailed guide
- `deployment/DEPLOYMENT_METHODS.md` - Method comparison

---

**Need more help?** Check `RENDER_DEPLOYMENT.md` for detailed instructions.
