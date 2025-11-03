import json
import sys
import os

# Add shared directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from utils import detect_language, get_translation, get_ai_response

def handler(req):
    """Vercel serverless function for chat endpoint"""
    # Handle CORS headers
    cors_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    # Handle preflight
    if req.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }
    
    try:
        # Parse request body
        if hasattr(req, 'json') and req.json:
            data = req.json
        elif hasattr(req, 'body'):
            body = req.body
            if isinstance(body, str):
                data = json.loads(body) if body else {}
            elif isinstance(body, bytes):
                data = json.loads(body.decode('utf-8')) if body else {}
            else:
                data = body if body else {}
        else:
            data = {}
        
        message = data.get('message', '').strip()
        reply_lang = data.get('reply_lang', 'ti')
        
        if not message:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({'success': False, 'error': 'No message provided'})
            }
        
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
        detected_lang = detect_language(message)
        is_tigrinya_input = (detected_lang == 'ti')
        
        # Step 2: If input is Tigrinya, ALWAYS translate to English first
        ai_input = message
        if is_tigrinya_input:
            english_input = get_translation(message, 'ti', 'en')
            if english_input:
                ai_input = english_input
                print(f"Translated Tigrinya input to English: {english_input}")
            else:
                print("Warning: Failed to translate Tigrinya input, using original")
        
        # Step 3: Get AI response
        enhanced_prompt = f"""Please provide a well-organized and clear response to the following question. Use proper formatting with:
- Clear headings for main topics (marked with **)
- Bullet points for lists
- Short paragraphs
- Proper spacing between sections

Question: {ai_input}"""
        
        ai_response = get_ai_response(enhanced_prompt)
        if not ai_response:
            import traceback
            last_error = traceback.format_exc() if hasattr(traceback, 'format_exc') else ''
            
            if '429' in last_error or 'ResourceExhausted' in last_error or 'quota' in last_error.lower():
                error_msg = "The AI service is temporarily rate-limited. Please wait a moment and try again in a few seconds."
            else:
                error_msg = "Sorry, I couldn't get a response from the AI. This might be due to:\n- API key issues\n- Network connectivity\n- API quota limits\n\nPlease wait a moment and try again."
            
            return {
                'statusCode': 503,
                'headers': cors_headers,
                'body': json.dumps({
                    'success': False,
                    'error': error_msg
                })
            }
        
        # Step 4: Translate AI response to reply language
        final_response = ai_response
        if reply_lang != 'en':
            translated_response = get_translation(ai_response, 'en', reply_lang)
            if translated_response:
                final_response = translated_response
                print(f"Translated AI response from English to {reply_lang}")
            else:
                print(f"Warning: Failed to translate to {reply_lang}, returning English")
        
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({
                'success': True,
                'response': final_response,
                'ai_response': ai_response,
                'translated_response': final_response,
                'reply_lang': reply_lang,
                'detected_input_lang': detected_lang
            })
        }
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'success': False, 'error': str(e)})
        }
