from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Set API key before importing utils
os.environ['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY', 'AIzaSyDxxKQoHOqeE9e2EKZ4O4Qtm70HnFfH5hw')

# Add shared directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from utils import detect_language, get_translation, get_ai_response, configure_gemini

# Reconfigure to ensure API key is set
configure_gemini()

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            if isinstance(body, bytes):
                data = json.loads(body.decode('utf-8'))
            else:
                data = json.loads(body) if body else {}
            
            message = data.get('message', '').strip()
            reply_lang = data.get('reply_lang', 'ti')
            
            if not message:
                response = {'success': False, 'error': 'No message provided'}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Get language names
            lang_names = {
                'en': 'English',
                'ti': 'Tigrinya',
                'no': 'Norwegian',
                'ar': 'Arabic',
                'am': 'Amharic'
            }
            
            # Detect if input is Tigrinya
            detected_lang = detect_language(message)
            is_tigrinya_input = (detected_lang == 'ti')
            
            # If input is Tigrinya, translate to English first
            ai_input = message
            if is_tigrinya_input:
                english_input = get_translation(message, 'ti', 'en')
                if english_input:
                    ai_input = english_input
                    print(f"Translated Tigrinya input to English: {english_input}")
            
            # Get AI response with timeout handling
            enhanced_prompt = f"""Please provide a well-organized and clear response to the following question. Use proper formatting with:
- Clear headings for main topics (marked with **)
- Bullet points for lists
- Short paragraphs
- Proper spacing between sections

Question: {ai_input}"""
            
            try:
                ai_response = get_ai_response(enhanced_prompt)
            except Exception as api_error:
                print(f"AI API error: {api_error}")
                error_msg = f"AI service error: {str(api_error)}"
                response = {'success': False, 'error': error_msg}
                self.wfile.write(json.dumps(response).encode())
                return
            
            if not ai_response:
                import traceback
                last_error = traceback.format_exc() if hasattr(traceback, 'format_exc') else ''
                
                if '429' in last_error or 'ResourceExhausted' in last_error or 'quota' in last_error.lower():
                    error_msg = "The AI service is temporarily rate-limited. Please wait a moment and try again in a few seconds."
                else:
                    error_msg = "Sorry, I couldn't get a response from the AI. This might be due to:\n- API key issues\n- Network connectivity\n- API quota limits\n\nPlease wait a moment and try again."
                
                response = {'success': False, 'error': error_msg}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Translate AI response to reply language
            final_response = ai_response
            if reply_lang != 'en':
                translated_response = get_translation(ai_response, 'en', reply_lang)
                if translated_response:
                    final_response = translated_response
                    print(f"Translated AI response from English to {reply_lang}")
            
            response = {
                'success': True,
                'response': final_response,
                'ai_response': ai_response,
                'translated_response': final_response,
                'reply_lang': reply_lang,
                'detected_input_lang': detected_lang
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Error in chat endpoint: {e}")
            import traceback
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'success': False, 'error': str(e)}
            self.wfile.write(json.dumps(response).encode())
