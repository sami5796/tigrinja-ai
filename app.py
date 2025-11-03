from flask import Flask, render_template, request, jsonify
from urllib.parse import quote
import os
from deep_translator import GoogleTranslator
import google.generativeai as genai

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create Flask app with explicit paths for templates and static files
# This ensures it works in Vercel's serverless environment
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static'),
    static_url_path='/static'
)

# Configure Gemini AI - use environment variable for cloud deployment
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDxxKQoHOqeE9e2EKZ4O4Qtm70HnFfH5hw')

# Validate API key exists
if not GEMINI_API_KEY or GEMINI_API_KEY.strip() == '':
    print("ERROR: GEMINI_API_KEY environment variable is not set!")
else:
    print(f"Gemini API key configured (length: {len(GEMINI_API_KEY)})")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("Gemini API configured successfully")
except Exception as e:
    print(f"ERROR configuring Gemini API: {e}")

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
    # For simplicity, we'll treat everything else as potentially English
    # In a production app, you'd use a proper language detection library
    return 'auto'  # Let Google Translate auto-detect

def get_translation(text, source_lang='en', target_lang='ti'):
    """Get translation from Google Translate using deep-translator library"""
    try:
        # Limit text length to prevent timeouts (Vercel has 10s timeout)
        # Translate in chunks if too long
        max_length = 1000  # Reasonable chunk size
        if len(text) > max_length:
            print(f"Text too long ({len(text)} chars), truncating to {max_length}")
            text = text[:max_length] + "..."
        
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
            except Exception as e2:
                print(f"Fallback translation also failed: {e2}")
                pass
        return None

def get_google_translate_url(text, source_lang='en', target_lang='ti'):
    """Get Google Translate URL (for client-side opening)"""
    try:
        translate_url = f"https://translate.google.no/?sl={source_lang}&tl={target_lang}&text={quote(text)}&op=translate"
        return translate_url
    except Exception as e:
        print(f"Error generating translate URL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        reply_lang = data.get('reply_lang', 'ti')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Auto-detect source language
        detected_lang = detect_language(text)
        source_lang = detected_lang if detected_lang != 'auto' else 'auto'
        
        # Get translation first
        translation = get_translation(text, source_lang, reply_lang)
        
        # Generate URL for client-side opening (cloud-compatible)
        source_for_url = source_lang if source_lang != 'auto' else 'auto'
        translate_url = get_google_translate_url(text, source_for_url, reply_lang)
        
        if translation:
            return jsonify({
                'success': True,
                'translation': translation,
                'original': text,
                'reply_lang': reply_lang,
                'translate_url': translate_url,
                'message': 'Translation completed!'
            })
        else:
            return jsonify({
                'success': True,
                'translation': None,
                'original': text,
                'reply_lang': reply_lang,
                'translate_url': translate_url,
                'message': 'Opening Google Translate in browser...'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_ai_response(message):
    """Get AI response from Gemini"""
    import time
    
    # Retry logic for rate limits (reduced delays for Vercel timeout)
    max_retries = 2  # Reduced from 3 to save time
    retry_delay = 1  # Reduced from 2 seconds
    
    print(f"[AI] Starting get_ai_response, max_retries: {max_retries}")
    
    for attempt in range(max_retries):
        try:
            print(f"[AI] Attempt {attempt + 1}/{max_retries}")
            attempt_start = time.time()
            
            # Get available model (with caching)
            print(f"[AI] Getting available model...")
            model_name = get_available_model()
            if not model_name:
                print("[AI] ERROR: No available Gemini model found")
                return None
            
            print(f"[AI] Using model: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            # Generate content
            print(f"[AI] Calling generate_content...")
            gen_start = time.time()
            response = model.generate_content(message)
            gen_time = time.time() - gen_start
            print(f"[AI] generate_content took {gen_time:.2f}s")
            
            # Handle different response formats
            print(f"[AI] Processing response...")
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
            print(f"[AI] Response attributes: {dir(response)}")
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
            
            attempt_time = time.time() - attempt_start
            print(f"[AI] Attempt {attempt + 1} failed after {attempt_time:.2f}s")
            
            if is_rate_limit and attempt < max_retries - 1:
                # Wait before retrying
                wait_time = retry_delay * (attempt + 1)
                print(f"[AI] ⏳ Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                continue
            
            print(f"[AI] ❌ Error (attempt {attempt + 1}/{max_retries}): {error_type}: {error_msg}")
            
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

@app.route('/api/chat', methods=['POST'])
def chat():
    import time
    start_time = time.time()
    request_id = f"{int(time.time() * 1000)}"
    
    try:
        print(f"\n{'='*60}")
        print(f"[{request_id}] NEW CHAT REQUEST")
        print(f"{'='*60}")
        
        data = request.get_json()
        print(f"[{request_id}] Request data received: {bool(data)}")
        
        if not data:
            print(f"[{request_id}] ERROR: No JSON data in request")
            return jsonify({'error': 'No data provided', 'request_id': request_id}), 400
        
        message = data.get('message', '').strip()
        reply_lang = data.get('reply_lang', 'ti')
        
        print(f"[{request_id}] Message: {message[:50]}... (length: {len(message)})")
        print(f"[{request_id}] Reply language: {reply_lang}")
        
        if not message:
            print(f"[{request_id}] ERROR: Empty message")
            return jsonify({'error': 'No message provided', 'request_id': request_id}), 400
        
        # Get language names for display
        lang_names = {
            'en': 'English',
            'ti': 'Tigrinya',
            'no': 'Norwegian',
            'ar': 'Arabic',
            'am': 'Amharic'
        }
        reply_name = lang_names.get(reply_lang, reply_lang)
        
        # Step 1: Detect if input is Tigrinya
        print(f"[{request_id}] Step 1: Detecting language...")
        detected_lang = detect_language(message)
        is_tigrinya_input = (detected_lang == 'ti')
        print(f"[{request_id}] Detected language: {detected_lang}, Is Tigrinya: {is_tigrinya_input}")
        
        # Step 2: If input is Tigrinya, ALWAYS translate to English first using Google Translate
        ai_input = message
        if is_tigrinya_input:
            print(f"[{request_id}] Step 2: Translating Tigrinya to English...")
            translation_start = time.time()
            # Translate Tigrinya input to English for AI
            english_input = get_translation(message, 'ti', 'en')
            translation_time = time.time() - translation_start
            print(f"[{request_id}] Translation took {translation_time:.2f}s")
            if english_input:
                ai_input = english_input
                print(f"[{request_id}] Translated: {english_input[:50]}...")
            else:
                # If translation fails, try with original message
                print(f"[{request_id}] WARNING: Translation failed, using original")
        
        # Step 3: Get AI response (always in English)
        # Ask AI to format response nicely
        enhanced_prompt = f"""Please provide a well-organized and clear response to the following question. Use proper formatting with:
- Clear headings for main topics (marked with **)
- Bullet points for lists
- Short paragraphs
- Proper spacing between sections

Question: {ai_input}"""
        
        print(f"[{request_id}] Step 3: Calling AI (prompt length: {len(enhanced_prompt)})...")
        ai_start = time.time()
        try:
            ai_response = get_ai_response(enhanced_prompt)
            ai_time = time.time() - ai_start
            print(f"[{request_id}] AI call took {ai_time:.2f}s")
        except Exception as e:
            ai_time = time.time() - ai_start
            print(f"[{request_id}] EXCEPTION in get_ai_response after {ai_time:.2f}s: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            ai_response = None
        
        print(f"[{request_id}] AI response received: {ai_response is not None}")
        if ai_response:
            print(f"[{request_id}] AI response length: {len(ai_response)} chars")
            print(f"[{request_id}] AI response preview: {ai_response[:100]}...")
        else:
            print(f"[{request_id}] ERROR: No AI response received")
        
        if not ai_response:
            # Provide a helpful error message based on what might have happened
            # Check if it's likely a rate limit issue
            import traceback
            last_error = traceback.format_exc() if hasattr(traceback, 'format_exc') else ''
            
            if '429' in last_error or 'ResourceExhausted' in last_error or 'quota' in last_error.lower():
                error_msg = "The AI service is temporarily rate-limited. Please wait a moment and try again in a few seconds."
            elif 'timeout' in last_error.lower() or 'timed out' in last_error.lower():
                error_msg = "The request timed out. Please try with a shorter message or try again."
            else:
                error_msg = "Sorry, I couldn't get a response from the AI. This might be due to:\n- API key issues\n- Network connectivity\n- API quota limits\n- Request timeout\n\nPlease try again with a shorter message."
            
            return jsonify({
                'success': False,
                'error': error_msg
            }), 503  # Service Unavailable instead of 500
        
        # Step 4: Translate AI response to reply language using Google Translate
        # Use try/except to handle translation timeouts gracefully
        final_response = ai_response
        if reply_lang != 'en':
            print(f"[{request_id}] Step 4: Translating to {reply_lang}...")
            translation_start = time.time()
            try:
                # Always translate using Google Translate (especially important for Tigrinya)
                translated_response = get_translation(ai_response, 'en', reply_lang)
                translation_time = time.time() - translation_start
                print(f"[{request_id}] Translation took {translation_time:.2f}s")
                if translated_response:
                    final_response = translated_response
                    print(f"[{request_id}] Successfully translated to {reply_lang}")
                else:
                    # If translation fails, return English response
                    print(f"[{request_id}] WARNING: Translation returned None, using English")
            except Exception as e:
                translation_time = time.time() - translation_start
                # If translation times out or fails, return English response
                print(f"[{request_id}] Translation ERROR after {translation_time:.2f}s: {type(e).__name__}: {e}")
                final_response = ai_response
        else:
            print(f"[{request_id}] Step 4: Skipping translation (reply_lang is 'en')")
        
        # Format response for display
        response_text = final_response
        total_time = time.time() - start_time
        
        print(f"[{request_id}] ✅ SUCCESS - Total time: {total_time:.2f}s")
        print(f"[{request_id}] Response length: {len(response_text)} chars")
        print(f"{'='*60}\n")
        
        return jsonify({
            'success': True,
            'response': response_text,
            'ai_response': ai_response,  # Keep original English AI response for reference
            'translated_response': final_response,
            'reply_lang': reply_lang,
            'detected_input_lang': detected_lang,
            'request_id': request_id,
            'processing_time': round(total_time, 2)
        })
    
    except Exception as e:
        total_time = time.time() - start_time
        error_type = type(e).__name__
        error_msg = str(e)
        
        print(f"[{request_id}] ❌ EXCEPTION after {total_time:.2f}s")
        print(f"[{request_id}] Error type: {error_type}")
        print(f"[{request_id}] Error message: {error_msg}")
        import traceback
        print(f"[{request_id}] Traceback:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        return jsonify({
            'error': f'{error_type}: {error_msg}',
            'request_id': request_id,
            'processing_time': round(total_time, 2)
        }), 500

# For Vercel deployment, the app will be served via serverless functions
# For local development, run this directly
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug, host='0.0.0.0', port=port)

