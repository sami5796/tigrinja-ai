from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import quote

# Add shared directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from utils import detect_language, get_translation

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
            
            text = data.get('text', '').strip()
            reply_lang = data.get('reply_lang', 'ti')
            
            if not text:
                response = {'success': False, 'error': 'No text provided'}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Auto-detect source language
            detected_lang = detect_language(text)
            source_lang = detected_lang if detected_lang != 'auto' else 'auto'
            
            # Get translation
            translation = get_translation(text, source_lang, reply_lang)
            
            # Generate Google Translate URL
            source_for_url = source_lang if source_lang != 'auto' else 'auto'
            translate_url = f"https://translate.google.no/?sl={source_for_url}&tl={reply_lang}&text={quote(text)}&op=translate"
            
            if translation:
                response = {
                    'success': True,
                    'translation': translation,
                    'original': text,
                    'reply_lang': reply_lang,
                    'translate_url': translate_url,
                    'message': 'Translation completed!'
                }
            else:
                response = {
                    'success': True,
                    'translation': None,
                    'original': text,
                    'reply_lang': reply_lang,
                    'translate_url': translate_url,
                    'message': 'Opening Google Translate in browser...'
                }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Error in translate endpoint: {e}")
            import traceback
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'success': False, 'error': str(e)}
            self.wfile.write(json.dumps(response).encode())
