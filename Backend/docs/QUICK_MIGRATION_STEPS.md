# ⚡ Quick Migration Steps - NeonDB to Supabase

## 🎯 You're Already Using PostgreSQL!

Your app uses PostgreSQL (NeonDB), so migrating to Supabase is just **changing the connection string**. No code changes needed!

---

## 📝 5-Minute Migration

### 1️⃣ Create Supabase Project
- Go to https://supabase.com
- Click "New Project"
- Name: `AeroGuard`
- Set strong password (SAVE IT!)
- Choose region
- Wait 2 minutes

### 2️⃣ Get Connection String
- Dashboard → Settings → Database
- Copy **URI** connection string
- Replace `[YOUR-PASSWORD]` with your actual password

Example:
```
postgresql://postgres.abcdefgh:MyPass123@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### 3️⃣ Update .env File
Open `Backend/.env` and replace:

```env
# OLD
DATABASE_URL=postgresql://neondb_owner:xxxxx@ep-xxx.aws.neon.tech/neondb?sslmode=require

# NEW (your Supabase connection string)
DATABASE_URL=postgresql://postgres.xxxxx:YourPassword@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### 4️⃣ Initialize Database
```bash
cd "d:\VS-Code projects\AeroGuard_\Backend"
python init_db.py
```

### 5️⃣ (Optional) Add Sample Data
```bash
python init_db.py --seed
```

### 6️⃣ Test
```bash
python run.py
```

Visit: http://localhost:5000/api/health

---

## ✅ Done!

Check Supabase Dashboard → Table Editor to see your tables:
- users
- locations
- sensors
- aqi_data
- forecasts
- user_preferences
- user_locations
- model_metrics

---

## 🆘 Quick Troubleshooting

**Can't connect?**
- Check password is correct
- Verify connection string format
- Ensure internet connection

**Tables not created?**
- Run `python init_db.py` again
- Check terminal for error messages

**Need detailed help?**
- Read `SUPABASE_MIGRATION_GUIDE.md` for full explanation

---

## 🎁 Bonus: What You Get with Supabase

- ✅ PostgreSQL database (same as before)
- ✅ Better dashboard with SQL editor
- ✅ Automatic daily backups
- ✅ Built-in authentication (optional)
- ✅ Real-time subscriptions (optional)
- ✅ File storage (optional)
- ✅ Auto-generated REST API (optional)

All your existing code works as-is! 🎉
