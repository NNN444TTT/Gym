# Gym Tracker - Deployment Guide

## 🚀 Quick Deployment Options

### **RECOMMENDED: Railway (Easiest)**

1. **Install Railway CLI**
   ```bash
   npm install -g railway
   ```

2. **Login & Deploy**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables** (in Railway dashboard)
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app
   ```

4. **Done!** Your app is live at `https://your-app.railway.app`

---

### **Alternative: PythonAnywhere (Also Easy)**

1. **Sign up** at https://www.pythonanywhere.com (free)

2. **Upload your code** via Git or zip

3. **Create web app**:
   - Choose Django
   - Python 3.11
   - Point to your project

4. **Set environment variables** in web tab

5. **Reload** and visit your-username.pythonanywhere.com

---

### **Alternative: Fly.io (Modern & Fast)**

1. **Install Fly CLI**
   ```bash
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login & Launch**
   ```bash
   fly auth login
   fly launch
   ```

3. **Set secrets**
   ```bash
   fly secrets set SECRET_KEY=your-secret-key
   fly secrets set DEBUG=False
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

---

## 🏠 Self-Hosting on Your Computer

### **Setup**

1. **Generate a secret key**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Create `.env` file** (at project root)
   ```
   SECRET_KEY=your-generated-key
   DEBUG=False
   ALLOWED_HOSTS=your-ip-address,yourdomain.com
   ```

3. **Install production dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Run with Gunicorn** (production server)
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8080
   ```

### **Router Configuration**

1. **Port Forward**: Forward external port 8080 → your computer's port 8080
2. **Find your public IP**: Visit https://whatismyipaddress.com
3. **Dynamic DNS** (optional): Use services like No-IP or DuckDNS if your IP changes
4. **Firewall**: Allow port 8080 in Windows Firewall

### **Users Access Via**
```
http://YOUR_PUBLIC_IP:8080
```

---

## 📊 Data Storage

### **Current Setup (SQLite)**
- ✅ Perfect for 3-4 users
- ✅ File stored at `db.sqlite3` in project root
- ✅ No separate database server needed
- ✅ Simple backups (just copy the file)
- ⚠️ Not ideal for 100+ concurrent users (but you don't need that)

### **Backup Strategy**
```bash
# Manual backup
copy db.sqlite3 backups\db_backup_2026-02-10.sqlite3

# Automated daily backup (Windows Task Scheduler)
copy C:\path\to\Gym\db.sqlite3 C:\backups\db_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sqlite3
```

---

## 🔒 Security Checklist

- [x] Use environment variables for SECRET_KEY
- [x] Set DEBUG=False in production
- [x] Configure ALLOWED_HOSTS properly
- [x] Use HTTPS (free with Railway/Fly.io/PythonAnywhere)
- [x] WhiteNoise for static files
- [x] Security headers enabled
- [ ] Consider adding proper authentication (passwords) for production
- [ ] Set up SSL certificate if self-hosting

---

## 📦 GitHub Setup (Optional but Recommended)

### **Why Use GitHub?**
- Easy deployment to Railway/Fly.io/Render
- Version control
- Backup of your code
- Easy rollbacks if something breaks

### **Setup**

1. **Create `.gitignore`**
   ```
   db.sqlite3
   __pycache__/
   *.pyc
   staticfiles/
   .env
   *.log
   ```

2. **Initialize Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Gym Tracker"
   ```

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/yourusername/gym-tracker.git
   git push -u origin main
   ```

4. **Deploy from GitHub** (Railway/Fly.io can auto-deploy on push!)

---

## 💡 My Recommendation for You

**For 3-4 users, I recommend:**

1. **Railway or Fly.io** (free tier)
   - Always online
   - HTTPS automatic
   - No need to keep your PC on
   - SQLite works perfectly
   - Deploy in 5 minutes

2. **Keep SQLite** - more than enough for 3-4 users

3. **Use GitHub** - makes deployment super easy

4. **Automated backups** - Railway/Fly.io have volume snapshots

---

## 🎯 Quickest Path to Production

```bash
# 1. Install Railway CLI
npm install -g railway

# 2. Initialize
railway login
railway init

# 3. Generate secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 4. Set environment variables in Railway dashboard
# SECRET_KEY=<generated-key>
# DEBUG=False

# 5. Deploy
railway up

# 6. Create superuser (via Railway shell)
railway run python manage.py migrate
railway run python manage.py createsuperuser

# Done! 🎉
```

---

## 📱 How Users Will Access

- **Cloud Hosting**: `https://your-app.railway.app`
- **Self-Hosting**: `http://YOUR_PUBLIC_IP:8080`

Both work great - cloud hosting is just easier and more reliable!

---

## 💾 Where is Data Stored?

### **Cloud Hosting**
- SQLite file stored on hosting platform's persistent volume
- Survives restarts/deploys
- Automatic backups available

### **Self-Hosting**
- SQLite file on your computer at `C:\Users\Natal\OneDrive\Projects\Gym\db.sqlite3`
- You control backups
- Consider using OneDrive/Dropbox for automatic cloud backup

---

## 🔄 Scaling Later (If Needed)

If you grow beyond 3-4 users:
1. Switch to PostgreSQL (easy with Railway/Fly.io)
2. Keep using same hosting platform
3. Minimal code changes needed

But honestly, SQLite + Railway/Fly.io will work perfectly for your use case!
