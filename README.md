# ዝሓስብ ኮምፒተር ብ´ትግርኛ | Tigrinja AI

A modern, user-friendly AI chatbot interface for multilingual communication with Tigrinya support. Built with Flask, Google Gemini AI, and featuring a beautiful, glassmorphic full-screen UI.

## ✨ Features

- 🤖 **AI Chatbot** - Powered by Google Gemini AI with intelligent multilingual support
- 🌐 **Auto Translation** - Automatic translation between Tigrinya, English, Norwegian, Arabic, and Amharic
- 🎨 **Modern UI** - Full-screen glassmorphic design with subtle neon effects
- 🌍 **Multilingual UI** - Interface available in Tigrinya, English, and Norwegian
- 📱 **Fully Responsive** - Optimized for desktop, tablet, and mobile devices
- ⚡ **Smart Language Detection** - Automatically detects input language
- 🔄 **Inline Thinking Indicator** - Shows "ይሓስብ..." (thinking...) instead of full-screen loading

## 🚀 Quick Start

### Option 1: Run from GitHub (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/tigrinja-ai.git
cd tigrinja-ai
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up your Gemini API key (optional for local dev):**
```bash
export GEMINI_API_KEY="your-api-key-here"  # On Windows: set GEMINI_API_KEY=your-api-key-here
```

5. **Run the Flask application:**
```bash
python app.py
```

6. **Open your browser:**
Navigate to `http://localhost:5001`

### Option 2: Install Locally

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variable (optional):**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

3. **Run the application:**
```bash
python app.py
```

## 📋 Requirements

- Python 3.8 or higher
- Google Gemini API Key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))

## 🌐 Deployment to Cloud

This application can run completely in the cloud! Recommended platforms:

- **Heroku** - Easy setup with free tier
- **Railway** - Modern interface, great free tier
- **Render** - Automatic deployments
- **PythonAnywhere** - Beginner-friendly
- **AWS/Azure/GCP** - For production scaling

### Environment Variables for Cloud Deployment

Set these in your cloud platform's environment settings:

- `GEMINI_API_KEY` - Your Google Gemini API key (required)

The app will automatically use the port provided by the cloud platform.

## 📖 Usage

1. **Select Reply Language:** Choose your preferred language for AI responses (Tigrinya, English, Norwegian, Arabic, or Amharic)
2. **Type Your Message:** Enter your question in any supported language
3. **AI Response:** The AI will:
   - Auto-detect your input language
   - Translate Tigrinya input to English for AI processing
   - Generate a response
   - Translate the response to your chosen reply language
4. **Translate Feature:** Use the translate button to open Google Translate in your browser

## 🎯 Supported Languages

### UI Languages:
- ትግርኛ (Tigrinya) - Default
- English
- Norsk (Norwegian)

### Reply/Translation Languages:
- ትግርኛ (Tigrinya)
- English
- Norsk (Norwegian)
- Arabic (العربية)
- Amharic (አማርኛ)

## 📁 Project Structure

```
.
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── templates/
│   └── index.html         # Main HTML template
└── static/
    ├── css/
    │   └── style.css      # Styling (glassmorphic design)
    └── js/
        ├── script.js      # JavaScript functionality
        └── i18n.js        # Internationalization
```

## 🛠️ Technologies Used

- **Flask** - Web framework
- **Google Gemini AI** - AI responses
- **Google Translate** (via deep-translator) - Translation service
- **HTML5/CSS3** - Modern UI with glassmorphism
- **JavaScript** - Interactive functionality and i18n

## 🔒 Security Notes

- ⚠️ **Never commit your API keys to GitHub**
- Use environment variables for sensitive data
- The default API key in `app.py` is for local development only
- For production, always use environment variables

## 🐛 Troubleshooting

**Server won't start:**
- Check if port 5001 is available
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**API errors:**
- Verify your `GEMINI_API_KEY` is set correctly
- Check API quota limits at [Google AI Studio](https://makersuite.google.com/app/apikey)

**Translation not working:**
- Ensure you have internet connection (uses Google Translate API)
- Check browser console for errors

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Made with ❤️ for the Tigrinya-speaking community**
