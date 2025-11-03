import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

def handler(req):
    try:
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
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': True, 'message': 'Test handler works', 'data': data})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': False, 'error': str(e)})
        }
