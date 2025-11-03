# 🚀 GitHub Setup Guide

This guide will help you set up your Tigrinja-AI project on GitHub and run it from there.

## Step 1: Initialize Git Repository (if not already done)

```bash
cd "/Users/user/Documents/Tig auto translate "
git init
```

## Step 2: Add Files to Git

```bash
git add .
git commit -m "Initial commit: Tigrinja-AI chatbot"
```

## Step 3: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `tigrinja-ai` or `tigrinya-chatbot`
3. **Don't** initialize it with README, .gitignore, or license (we already have these)

## Step 4: Connect Local Repository to GitHub

```bash
# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 5: Clone and Run from GitHub (Anywhere)

Once your code is on GitHub, anyone (including you on another computer) can run it:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# (Optional) Set your API key
export GEMINI_API_KEY="your-api-key-here"

# Run the app
python app.py
```

## 🔒 Important: API Key Security

⚠️ **Your API key is currently in the code for local development only.**

For production/cloud deployment:

1. **Remove the default API key** from `app.py` or use environment variables
2. **Set the API key as an environment variable:**
   ```bash
   export GEMINI_API_KEY="your-actual-key"
   ```
3. **On cloud platforms**, set it in their environment variable settings

## 📝 What's Ready for GitHub?

✅ `.gitignore` - Excludes sensitive files and venv  
✅ `README.md` - Comprehensive documentation  
✅ `requirements.txt` - All dependencies  
✅ `setup.sh` - Easy setup script  
✅ `Procfile` - For cloud deployment (Heroku, Railway, etc.)  
✅ Environment variable support in `app.py`  

## 🚀 Next Steps

1. Push your code to GitHub
2. Share the repository URL with others
3. Deploy to cloud platforms using the Procfile
4. Enjoy running your app from anywhere!

## 💡 Quick Test

After pushing to GitHub, test cloning it:

```bash
cd /tmp  # or any other directory
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
./setup.sh
python app.py
```

If it works, you're all set! 🎉

