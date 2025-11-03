import os
import time
from deep_translator import GoogleTranslator
import google.generativeai as genai

# Configure Gemini AI - Get API key from environment variable
# Reconfigure on each import to ensure it's fresh
def configure_gemini():
    # Try environment variable first, then fallback to default
    api_key = os.environ.get('GEMINI_API_KEY') or 'AIzaSyDxxKQoHOqeE9e2EKZ4O4Qtm70HnFfH5hw'
    if api_key:
        try:
            genai.configure(api_key=api_key)
            print(f"Gemini API configured with key: {api_key[:20]}...")
            return True
        except Exception as e:
            print(f"Error configuring Gemini API: {e}")
            return False
    return False

# Initial configuration
configure_gemini()

# Cache available model name
AVAILABLE_MODEL = None

def get_available_model():
    """Get an available Gemini model"""
    global AVAILABLE_MODEL
    if AVAILABLE_MODEL:
        return AVAILABLE_MODEL
    
    try:
        # List all available models
        models = genai.list_models()
        # Prefer newer, faster models
        preferred = ['models/gemini-2.0-flash', 'models/gemini-flash-latest', 'models/gemini-2.5-flash']
        
        for pref in preferred:
            for model in models:
                if model.name == pref and 'generateContent' in model.supported_generation_methods:
                    AVAILABLE_MODEL = pref
                    print(f"Found available model: {pref}")
                    return pref
        
        # If preferred not found, use first available
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                AVAILABLE_MODEL = model.name
                print(f"Using available model: {model.name}")
                return model.name
    except Exception as e:
        print(f"Error listing models: {e}")
    
    # Ultimate fallback
    fallback = 'models/gemini-2.0-flash'
    AVAILABLE_MODEL = fallback
    print(f"Using fallback model: {fallback}")
    return fallback

def detect_language(text):
    """Detect if text is in Tigrinya (Ge'ez script)"""
    # Tigrinya uses Ge'ez script - Unicode range: U+1200–U+137F
    tigrinya_range = range(0x1200, 0x1380)
    for char in text:
        if ord(char) in tigrinya_range:
            return 'ti'
    # If no Tigrinya characters found, assume it's English or other
    return 'auto'  # Let Google Translate auto-detect

def get_translation(text, source_lang='en', target_lang='ti'):
    """Get translation from Google Translate using deep-translator library"""
    try:
        # Use deep-translator which uses HTTP requests (no browser needed)
        # If source_lang is 'auto', Google Translate will auto-detect
        if source_lang == 'auto':
            # Try to detect manually first (for Tigrinya)
            detected = detect_language(text)
            if detected == 'ti':
                source_lang = 'ti'
            else:
                # For auto-detection, we'll use 'auto' if supported, otherwise try common languages
                source_lang = 'auto'
        
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translation = translator.translate(text)
        return translation if translation else None
    except Exception as e:
        print(f"Error getting translation: {e}")
        # Try with auto-detection if initial attempt failed
        if source_lang != 'auto':
            try:
                translator = GoogleTranslator(source='auto', target=target_lang)
                translation = translator.translate(text)
                return translation if translation else None
            except:
                pass
        return None

def get_ai_response(message):
    """Get AI response from Gemini using REST API (works better in serverless)"""
    import requests
    
    # Ensure API is configured
    configure_gemini()
    
    # Get API key
    api_key = os.environ.get('GEMINI_API_KEY') or 'AIzaSyDxxKQoHOqeE9e2EKZ4O4Qtm70HnFfH5hw'
    
    # Retry logic
    max_retries = 2
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Use REST API directly (more reliable in serverless environments)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": message}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048
                }
            }
            
            print(f"Calling Gemini REST API (attempt {attempt + 1}/{max_retries})...")
            response = requests.post(url, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                # Extract text from response
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        if len(candidate['content']['parts']) > 0:
                            text = candidate['content']['parts'][0].get('text', '').strip()
                            if text:
                                print("✓ AI response received via REST API")
                                return text
            
            # Handle errors
            if response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    print(f"Rate limit hit, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
            
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            error_msg = error_data.get('error', {}).get('message', f"HTTP {response.status_code}")
            print(f"API error: {error_msg}")
            
            # Try SDK fallback if REST fails
            if attempt == max_retries - 1:
                print("Trying SDK fallback...")
                try:
                    model = genai.GenerativeModel('models/gemini-2.0-flash')
                    sdk_response = model.generate_content(message)
                    if hasattr(sdk_response, 'text') and sdk_response.text:
                        return sdk_response.text.strip()
                except Exception as sdk_error:
                    print(f"SDK fallback also failed: {sdk_error}")
            
            return None
            
        except requests.exceptions.Timeout:
            print(f"Request timeout (attempt {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return None
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error getting AI response (attempt {attempt + 1}/{max_retries}): {error_msg}")
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            
            # Try SDK as last resort
            try:
                model = genai.GenerativeModel('models/gemini-2.0-flash')
                sdk_response = model.generate_content(message)
                if hasattr(sdk_response, 'text') and sdk_response.text:
                    return sdk_response.text.strip()
            except:
                pass
            
            return None
    
    return None

