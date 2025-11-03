import os
import time
from deep_translator import GoogleTranslator
import google.generativeai as genai

# Configure Gemini AI - Get API key from environment variable
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDxxKQoHOqeE9e2EKZ4O4Qtm70HnFfH5hw')
genai.configure(api_key=GEMINI_API_KEY)

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
    """Get AI response from Gemini"""
    # Retry logic for rate limits
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # Get available model (with caching)
            model_name = get_available_model()
            if not model_name:
                print("No available Gemini model found")
                return None
            
            model = genai.GenerativeModel(model_name)
            
            # Generate content
            response = model.generate_content(message)
            
            # Handle different response formats
            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            elif hasattr(response, 'candidates') and response.candidates:
                if len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content:
                        if hasattr(candidate.content, 'parts') and candidate.content.parts:
                            return candidate.content.parts[0].text.strip()
            
            print("Warning: Empty response from Gemini")
            return None
            
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            
            # Check if it's a rate limit error
            is_rate_limit = (
                'ResourceExhausted' in error_type or 
                '429' in error_msg or 
                'quota' in error_msg.lower() or 
                'rate limit' in error_msg.lower() or
                'Resource exhausted' in error_msg
            )
            
            if is_rate_limit and attempt < max_retries - 1:
                # Wait before retrying
                wait_time = retry_delay * (attempt + 1)
                print(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                continue
            
            print(f"Error getting AI response (attempt {attempt + 1}/{max_retries}): {error_msg}")
            
            # Reset model cache if it fails
            global AVAILABLE_MODEL
            AVAILABLE_MODEL = None
            
            # Provide helpful error messages
            if 'API key' in error_msg or 'authentication' in error_msg.lower():
                print("API key authentication error - check your API key")
            elif is_rate_limit:
                print("API quota/rate limit exceeded - max retries reached")
            else:
                import traceback
                traceback.print_exc()
            
            # Return None to trigger error message in endpoint
            return None
    
    return None

