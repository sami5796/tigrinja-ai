"""Vercel serverless function for /api/chat endpoint"""
import sys
import os
import json
import time
from http.server import BaseHTTPRequestHandler

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.helpers import detect_language, get_translation, get_ai_response

class handler(BaseHTTPRequestHandler):
    """Handle /api/chat POST requests"""
    
    def do_POST(self):
        start_time = time.time()
        request_id = f"{int(time.time() * 1000)}"
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body) if body else {}
            except Exception as e:
                print(f"[{request_id}] Error parsing JSON: {e}")
                data = {}
            
            print(f"\n{'='*60}")
            print(f"[{request_id}] NEW CHAT REQUEST")
            print(f"{'='*60}")
            
            message = data.get('message', '').strip()
            reply_lang = data.get('reply_lang', 'ti')
            
            print(f"[{request_id}] Message: {message[:50]}... (length: {len(message)})")
            print(f"[{request_id}] Reply language: {reply_lang}")
            
            if not message:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No message provided', 'request_id': request_id}).encode('utf-8'))
                return
            
            # Step 1: Detect language
            print(f"[{request_id}] Step 1: Detecting language...")
            detected_lang = detect_language(message)
            is_tigrinya_input = (detected_lang == 'ti')
            print(f"[{request_id}] Detected language: {detected_lang}, Is Tigrinya: {is_tigrinya_input}")
            
            # Step 2: Translate Tigrinya input to English
            ai_input = message
            if is_tigrinya_input:
                print(f"[{request_id}] Step 2: Translating Tigrinya to English...")
                translation_start = time.time()
                english_input = get_translation(message, 'ti', 'en')
                translation_time = time.time() - translation_start
                print(f"[{request_id}] Translation took {translation_time:.2f}s")
                if english_input:
                    ai_input = english_input
                    print(f"[{request_id}] Translated: {english_input[:50]}...")
                else:
                    print(f"[{request_id}] WARNING: Translation failed, using original")
            
            # Step 3: Get AI response
            enhanced_prompt = f"""Please provide a well-organized and clear response to the following question. Use proper formatting with:
- Clear headings for main topics (marked with **)
- Bullet points for lists
- Short paragraphs
- Proper spacing between sections

Question: {ai_input}"""
            
            # Check time before AI call
            time_before_ai = time.time() - start_time
            if time_before_ai > 5.0:
                print(f"[{request_id}] ⚠️ Already used {time_before_ai:.2f}s - skipping AI call to avoid timeout")
                ai_response = "I apologize, but the request is taking too long. Please try again with a shorter message."
            else:
                print(f"[{request_id}] Step 3: Calling AI (time used: {time_before_ai:.2f}s)...")
                ai_start = time.time()
                try:
                    ai_response = get_ai_response(enhanced_prompt)
                    ai_time = time.time() - ai_start
                    print(f"[{request_id}] AI call took {ai_time:.2f}s")
                except Exception as e:
                    ai_time = time.time() - ai_start
                    print(f"[{request_id}] EXCEPTION in get_ai_response after {ai_time:.2f}s: {type(e).__name__}: {e}")
                    ai_response = None
            
            if not ai_response:
                error_msg = "Sorry, I couldn't get a response from the AI. This might be due to:\n- API key issues\n- Network connectivity\n- API quota limits\n- Request timeout\n\nPlease try again with a shorter message."
                
                self.send_response(503)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': error_msg
                }).encode('utf-8'))
                return
            
            # Step 4: Translate response
            total_time_so_far = time.time() - start_time
            time_remaining = 9.0 - total_time_so_far
            
            final_response = ai_response
            if reply_lang != 'en':
                if time_remaining < 2.0:
                    print(f"[{request_id}] Step 4: SKIPPING translation (only {time_remaining:.1f}s remaining)")
                else:
                    print(f"[{request_id}] Step 4: Translating to {reply_lang} ({time_remaining:.1f}s available)...")
                    translation_start = time.time()
                    try:
                        text_to_translate = ai_response
                        if time_remaining < 3.0 and len(text_to_translate) > 500:
                            text_to_translate = text_to_translate[:500] + "..."
                            print(f"[{request_id}] Truncating text for faster translation")
                        
                        translated_response = get_translation(text_to_translate, 'en', reply_lang)
                        translation_time = time.time() - translation_start
                        print(f"[{request_id}] Translation took {translation_time:.2f}s")
                        
                        if translated_response:
                            final_response = translated_response
                            print(f"[{request_id}] Successfully translated to {reply_lang}")
                        else:
                            print(f"[{request_id}] WARNING: Translation returned None, using English")
                    except Exception as e:
                        translation_time = time.time() - translation_start
                        print(f"[{request_id}] Translation ERROR after {translation_time:.2f}s: {type(e).__name__}: {e}")
                        final_response = ai_response
            
            total_time = time.time() - start_time
            print(f"[{request_id}] ✅ SUCCESS - Total time: {total_time:.2f}s")
            print(f"{'='*60}\n")
            
            response_data = {
                'success': True,
                'response': final_response,
                'ai_response': ai_response,
                'translated_response': final_response,
                'reply_lang': reply_lang,
                'detected_input_lang': detected_lang,
                'request_id': request_id,
                'processing_time': round(total_time, 2)
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        
        except Exception as e:
            total_time = time.time() - start_time
            error_type = type(e).__name__
            error_msg = str(e)
            
            print(f"[{request_id}] ❌ EXCEPTION after {total_time:.2f}s")
            print(f"[{request_id}] Error: {error_type}: {error_msg}")
            import traceback
            traceback.print_exc()
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f'{error_type}: {error_msg}',
                'request_id': request_id,
                'processing_time': round(total_time, 2)
            }).encode('utf-8'))
