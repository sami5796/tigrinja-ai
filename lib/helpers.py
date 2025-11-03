"""Shared helper functions for Vercel serverless functions"""
from urllib.parse import quote
import os
from deep_translator import GoogleTranslator
import google.generativeai as genai
import time

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDxxKQoHOqeE9e2EKZ4O4Qtm70HnFfH5hw')

# Initialize Gemini once (lazy loading)
_genai_configured = False

def configure_genai():
    """Configure Gemini AI (lazy initialization)"""
    global _genai_configured
    if not _genai_configured:
        if GEMINI_API_KEY and GEMINI_API_KEY.strip():
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                _genai_configured = True
                print(f"[INIT] Gemini API configured")
            except Exception as e:
                print(f"[INIT] ERROR configuring Gemini API: {e}")
        else:
            print("[INIT] ERROR: GEMINI_API_KEY not set!")

# Cache available model name
AVAILABLE_MODEL = None

def get_available_model():
    """Get an available Gemini model - optimized for speed"""
    global AVAILABLE_MODEL
    if AVAILABLE_MODEL:
        return AVAILABLE_MODEL
    
    # Use ONLY the fastest model directly
    AVAILABLE_MODEL = 'models/gemini-1.5-flash'
    print(f"[MODEL] Using model: {AVAILABLE_MODEL}")
    return AVAILABLE_MODEL

def detect_language(text):
    """Detect if text is in Tigrinya (Ge'ez script)"""
    tigrinya_range = range(0x1200, 0x1380)
    for char in text:
        if ord(char) in tigrinya_range:
            return 'ti'
    return 'auto'

def get_translation(text, source_lang='en', target_lang='ti'):
    """Get translation from Google Translate"""
    try:
        max_length = 1000
        if len(text) > max_length:
            print(f"Text too long ({len(text)} chars), truncating to {max_length}")
            text = text[:max_length] + "..."
        
        if source_lang == 'auto':
            detected = detect_language(text)
            if detected == 'ti':
                source_lang = 'ti'
        
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translation = translator.translate(text)
        return translation if translation else None
    except Exception as e:
        print(f"Error getting translation: {e}")
        if source_lang != 'auto':
            try:
                translator = GoogleTranslator(source='auto', target=target_lang)
                translation = translator.translate(text)
                return translation if translation else None
            except Exception as e2:
                print(f"Fallback translation also failed: {e2}")
        return None

def get_google_translate_url(text, source_lang='en', target_lang='ti'):
    """Get Google Translate URL"""
    try:
        translate_url = f"https://translate.google.no/?sl={source_lang}&tl={target_lang}&text={quote(text)}&op=translate"
        return translate_url
    except Exception as e:
        print(f"Error generating translate URL: {e}")
        return None

def get_ai_response(message):
    """Get AI response from Gemini with explicit timeout"""
    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
    
    # CRITICAL: Vercel timeout is 10s, we MUST finish in <3s for AI call
    MAX_AI_TIME = 3
    
    configure_genai()
    print(f"[AI] Starting get_ai_response, max_time: {MAX_AI_TIME}s")
    
    try:
        model_name = get_available_model()
        if not model_name:
            print("[AI] ERROR: No available Gemini model found")
            return None
        
        model = genai.GenerativeModel(model_name)
        
        generation_config = {
            'max_output_tokens': 128,
            'temperature': 0.7,
        }
        
        print(f"[AI] Calling generate_content with {MAX_AI_TIME}s timeout...")
        gen_start = time.time()
        
        def call_gemini():
            return model.generate_content(message, generation_config=generation_config)
        
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(call_gemini)
                try:
                    response = future.result(timeout=MAX_AI_TIME)
                    gen_time = time.time() - gen_start
                    print(f"[AI] generate_content completed in {gen_time:.2f}s")
                except FutureTimeoutError:
                    gen_time = time.time() - gen_start
                    print(f"[AI] ❌ TIMEOUT: generate_content exceeded {MAX_AI_TIME}s (took {gen_time:.2f}s)")
                    future.cancel()
                    return None
        except Exception as e:
            gen_time = time.time() - gen_start
            print(f"[AI] Exception after {gen_time:.2f}s: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        if not response:
            return None
        
        # Handle response formats
        if hasattr(response, 'text') and response.text:
            result = response.text.strip()
            print(f"[AI] ✅ Got response via .text (length: {len(result)})")
            return result
        elif hasattr(response, 'candidates') and response.candidates:
            if len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        result = candidate.content.parts[0].text.strip()
                        print(f"[AI] ✅ Got response via candidates (length: {len(result)})")
                        return result
        
        print("[AI] ⚠️ WARNING: Empty response from Gemini")
        return None
        
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"[AI] ❌ Error: {error_type}: {error_msg}")
        
        global AVAILABLE_MODEL
        AVAILABLE_MODEL = None
        
        return None

