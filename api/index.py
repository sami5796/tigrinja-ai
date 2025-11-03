"""Vercel serverless function for root route - serves HTML"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def handler(request):
    """Handle root route - serve HTML (Vercel Python format)"""
    try:
        # Read HTML file
        html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Replace Flask url_for with static paths
        html_content = html_content.replace("{{ url_for('static', filename='css/style.css') }}", '/static/css/style.css')
        html_content = html_content.replace("{{ url_for('static', filename='js/i18n.js') }}", '/static/js/i18n.js')
        html_content = html_content.replace("{{ url_for('static', filename='js/script.js') }}", '/static/js/script.js')
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8',
            },
            'body': html_content
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Error loading page: {str(e)}'
        }
