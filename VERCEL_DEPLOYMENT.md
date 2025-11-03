# 🚀 Vercel Deployment Guide

Your Tigrinja-AI app is now converted to **serverless functions** - no Flask needed! 

## ✨ What Changed

- ✅ **No Flask** - Removed Flask dependency
- ✅ **Serverless Functions** - `api/chat.py` and `api/translate.py`
- ✅ **Static Hosting** - Frontend files in `public/` directory
- ✅ **Simpler Deployment** - Just push to GitHub!

## 📁 New Project Structure

```
tigrinja-ai/
├── index.html              # Main HTML (moved from templates/)
├── public/                 # Static files (was static/)
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── script.js
│       └── i18n.js
├── api/                    # Serverless functions
│   ├── chat.py            # AI chat endpoint
│   └── translate.py       # Translation endpoint
├── shared/                 # Shared utilities
│   └── utils.py           # Common functions
├── vercel.json             # Vercel configuration
└── requirements.txt        # Python dependencies (no Flask!)
```

## 🚀 Deploy to Vercel (5 minutes)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Convert to Vercel serverless functions"
git push origin main
```

### Step 2: Connect to Vercel

1. **Go to [vercel.com](https://vercel.com)** and sign up/login with GitHub
2. **Click "Add New Project"**
3. **Import your repository:** `sami5796/tigrinja-ai`
4. **Vercel will auto-detect:**
   - Python serverless functions in `api/`
   - Static files in `public/`
   - Configuration from `vercel.json`

### Step 3: Set Environment Variable

1. In your Vercel project dashboard, go to **Settings** → **Environment Variables**
2. Add:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** Your Gemini API key
3. Click **Save**

### Step 4: Deploy!

1. Click **Deploy** (or it auto-deploys)
2. Wait ~2-3 minutes for build
3. Your app will be live at: `https://your-project-name.vercel.app`

## 🎯 That's It!

- ✅ **No Flask server to manage**
- ✅ **Auto-scales** with traffic
- ✅ **Free tier** available
- ✅ **Auto-deploys** from GitHub
- ✅ **Same functionality** - AI + Translation + UI

## 🔧 Local Development (Optional)

To test locally before deploying:

```bash
# Install Vercel CLI
npm install -g vercel

# Run locally
vercel dev
```

Then visit `http://localhost:3000`

## 📝 Environment Variables

In Vercel dashboard, set:
- `GEMINI_API_KEY` - Your Google Gemini API key

## 🐛 Troubleshooting

### Functions not working?
- Check that `GEMINI_API_KEY` is set in Vercel environment variables
- Verify `requirements.txt` has all dependencies
- Check Vercel function logs in dashboard

### Static files not loading?
- Ensure files are in `public/` directory
- Check that paths in `index.html` start with `/` (e.g., `/css/style.css`)

### CORS errors?
- CORS headers are already set in serverless functions
- Should work automatically

## 🎉 Benefits Over Flask

| Feature | Flask | Vercel Serverless |
|---------|-------|-------------------|
| **Deployment** | Manual setup | Auto from GitHub |
| **Scaling** | Manual | Automatic |
| **Cost** | Server 24/7 | Pay per request |
| **Complexity** | Full app | Just functions |
| **Cold Start** | N/A | ~100-300ms |
| **Free Tier** | Limited | Generous |

## 📚 Next Steps

1. ✅ Push code to GitHub
2. ✅ Connect to Vercel
3. ✅ Set environment variable
4. ✅ Deploy!
5. 🎉 Share your live app!

---

**Your app is now simpler, faster, and easier to deploy!** 🚀

