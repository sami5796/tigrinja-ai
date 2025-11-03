# 🚀 Cloud Deployment Guide

Your Tigrinja-AI app is ready to deploy! Choose one of these platforms:

## Option 1: Railway (Recommended - Easiest) ⭐

### Quick Deploy (5 minutes):

1. **Go to [Railway.app](https://railway.app)** and sign up/login with GitHub
2. **Click "New Project"** → **"Deploy from GitHub repo"**
3. **Select your repository:** `sami5796/tigrinja-ai`
4. **Add Environment Variable:**
   - Click on your project → **Variables** tab
   - Add: `GEMINI_API_KEY` = `your-api-key-here`
5. **Deploy!** Railway will automatically:
   - Detect Flask app
   - Install dependencies from `requirements.txt`
   - Use `Procfile` to run the app
   - Assign a public URL

### Your app will be live at: `https://your-app-name.railway.app`

---

## Option 2: Render (Free Tier Available)

### Deploy Steps:

1. **Go to [Render.com](https://render.com)** and sign up/login with GitHub
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository:** `sami5796/tigrinja-ai`
4. **Configure:**
   - **Name:** `tigrinja-ai` (or any name)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** `.` (leave blank)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. **Add Environment Variable:**
   - Scroll to **"Environment Variables"**
   - Add: `GEMINI_API_KEY` = `your-api-key-here`
   - Add: `PORT` (Render sets this automatically, but can add `8000` as fallback)
6. **Click "Create Web Service"**

### Your app will be live at: `https://tigrinja-ai.onrender.com`

---

## Option 3: Heroku

### Deploy Steps:

1. **Install Heroku CLI:**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku App:**
   ```bash
   cd "/Users/user/Documents/Tig auto translate "
   heroku create tigrinja-ai
   ```

4. **Set Environment Variable:**
   ```bash
   heroku config:set GEMINI_API_KEY=your-api-key-here
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

6. **Open your app:**
   ```bash
   heroku open
   ```

---

## Option 4: PythonAnywhere (Beginner-Friendly)

### Deploy Steps:

1. **Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)** (free account)
2. **Open a Bash console**
3. **Clone your repo:**
   ```bash
   git clone https://github.com/sami5796/tigrinja-ai.git
   cd tigrinja-ai
   ```
4. **Create virtual environment:**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. **Set environment variable:**
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
6. **Create Web App:**
   - Go to **Web** tab → **Add a new web app**
   - Choose **Flask**
   - Set Python version: **3.10**
   - Set source code directory: `/home/YOUR_USERNAME/tigrinja-ai`
   - WSGI file: `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`
7. **Edit WSGI file:**
   ```python
   import sys
   path = '/home/YOUR_USERNAME/tigrinja-ai'
   if path not in sys.path:
       sys.path.append(path)
   
   import os
   os.environ['GEMINI_API_KEY'] = 'your-api-key-here'
   
   from app import app as application
   ```

---

## ✅ Pre-Deployment Checklist

Before deploying, make sure:

- [x] ✅ Code is pushed to GitHub
- [x] ✅ `requirements.txt` is up to date
- [x] ✅ `Procfile` exists
- [x] ✅ `.gitignore` excludes sensitive files
- [ ] ⚠️ **Set `GEMINI_API_KEY` environment variable** (IMPORTANT!)
- [ ] ⚠️ **Test locally first**

---

## 🔒 Security Reminder

**NEVER commit your API key to GitHub!**

- ✅ Use environment variables on cloud platforms
- ✅ The default key in `app.py` is for local dev only
- ✅ Each platform has a way to set environment variables securely

---

## 🐛 Troubleshooting

### App won't start:
- Check that `GEMINI_API_KEY` is set correctly
- Verify `requirements.txt` has all dependencies
- Check platform logs for error messages

### 404 or "Not Found":
- Ensure port is set correctly (most platforms set `PORT` automatically)
- Check that `host='0.0.0.0'` in `app.py` (✅ already set)

### Translation not working:
- Check internet connectivity (needs Google Translate API)
- Verify no firewall blocking requests

---

## 📊 Platform Comparison

| Platform | Free Tier | Ease of Use | Auto-Deploy | Best For |
|----------|-----------|-------------|-------------|----------|
| **Railway** | ✅ Yes | ⭐⭐⭐⭐⭐ | ✅ Yes | Quick deployment |
| **Render** | ✅ Yes | ⭐⭐⭐⭐ | ✅ Yes | Free hosting |
| **Heroku** | ❌ Paid | ⭐⭐⭐ | ✅ Yes | Production apps |
| **PythonAnywhere** | ✅ Yes | ⭐⭐⭐ | ❌ Manual | Learning/testing |

---

## 🎉 After Deployment

Once deployed, your app will:
- ✅ Run 24/7 without your computer
- ✅ Be accessible from anywhere
- ✅ Auto-update when you push to GitHub (Railway/Render)
- ✅ Have a public URL to share

**Your Tigrinja-AI is now in the cloud! 🌟**

