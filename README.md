# ዝሓስብ ኮምፒተር ብ´ትግርኛ | Tigrinja AI

A modern, user-friendly AI chatbot that provides intelligent responses in Tigrinya, English, Norwegian, Arabic, and Amharic. Built with Flask and featuring a beautiful, glassmorphic UI.

## Features

- 🤖 **AI-Powered Chat**: Integrated with Google Gemini for intelligent responses
- 🌐 **Multilingual Support**: Auto-detects input language and translates responses
- 🎨 **Modern UI**: Glassmorphic design with neon accents, fully responsive
- 🔄 **Auto-Translation**: Tigrinya input → English (for AI) → Target language (for display)
- 📱 **Mobile-Friendly**: Optimized for all screen sizes

## Supported Languages

- **ትግርኛ** (Tigrinya)
- **English**
- **Norsk** (Norwegian)
- **Arabic**
- **Amharic**

## Local Development

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variable (optional for local dev):**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

3. **Run the Flask application:**
```bash
python app.py
```

4. **Open your browser:**
Navigate to `http://localhost:5001`

## Deployment to Vercel

### Prerequisites
- GitHub account
- Vercel account (with authorization already set up)

### Steps

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

2. **Deploy to Vercel:**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - **Set Environment Variable:**
     - Go to Project Settings → Environment Variables
     - Add `GEMINI_API_KEY` with your API key value
   - Click "Deploy"

3. **That's it!** Your app will be live at `https://your-project.vercel.app`

### Project Structure for Vercel

```
.
├── api/
│   └── index.py          # Vercel serverless function wrapper
├── app.py                # Main Flask application
├── templates/
│   └── index.html       # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── script.js
│       └── i18n.js
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── .gitignore          # Git ignore rules
```

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required for AI functionality)
- `PORT`: Server port (defaults to 5001 for local development)
- `FLASK_DEBUG`: Enable debug mode (defaults to True for local)

## Technologies Used

- **Flask** - Web framework
- **Google Gemini API** - AI responses
- **deep-translator** - Translation service
- **HTML5/CSS3** - Modern UI with glassmorphism
- **JavaScript** - Client-side interactions

## Notes

- The API key should be set as an environment variable in Vercel (never commit it to Git)
- The app automatically handles language detection and translation
- Tigrinya input is always translated to English for the AI, then back to the target language
- The UI is fully internationalized with support for Tigrinya, English, and Norwegian

## License

MIT License
