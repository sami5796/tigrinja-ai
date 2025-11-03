import json
import sys
import os
from urllib.parse import quote

# Add shared directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from utils import detect_language, get_translation

def handler(req):
    """Vercel serverless function for translate endpoint"""
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
        # Parse request body - Vercel Python functions receive body as string
        if hasattr(req, 'json') and req.json:
            data = req.json
        elif hasattr(req, 'body'):
            body = req.body
            if isinstance(body, str):
                data = json.loads(body) if body else {}
            else:
                data = body if body else {}
        else:
            data = {}
        
        text = data.get('text', '').strip()
        reply_lang = data.get('reply_lang', 'ti')
        
        if not text:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'success': False, 'error': 'No text provided'})
            }
        
        # Auto-detect source language
        detected_lang = detect_language(text)
        source_lang = detected_lang if detected_lang != 'auto' else 'auto'
        
        # Get translation first
        translation = get_translation(text, source_lang, reply_lang)
        
        # Generate Google Translate URL (client will open it)
        source_for_url = source_lang if source_lang != 'auto' else 'auto'
        translate_url = f"https://translate.google.no/?sl={source_for_url}&tl={reply_lang}&text={quote(text)}&op=translate"
        
        if translation:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'success': True,
                    'translation': translation,
                    'original': text,
                    'reply_lang': reply_lang,
                    'translate_url': translate_url,
                    'message': 'Translation completed!'
                })
            }
        else:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'success': True,
                    'translation': None,
                    'original': text,
                    'reply_lang': reply_lang,
                    'translate_url': translate_url,
                    'message': 'Opening Google Translate in browser...'
                })
            }
    
    except Exception as e:
        print(f"Error in translate endpoint: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'success': False, 'error': str(e)})
        }

