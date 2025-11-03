"""Vercel serverless function for root route - serves HTML"""
import sys
import os
from http.server import BaseHTTPRequestHandler

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class handler(BaseHTTPRequestHandler):
    """Handle root route - serve HTML"""
    
    def do_GET(self):
        try:
            # Read HTML file
            html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'index.html')
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Replace Flask url_for with static paths
            html_content = html_content.replace("{{ url_for('static', filename='css/style.css') }}", '/static/css/style.css')
            html_content = html_content.replace("{{ url_for('static', filename='js/i18n.js') }}", '/static/js/i18n.js')
            html_content = html_content.replace("{{ url_for('static', filename='js/script.js') }}", '/static/js/script.js')
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error loading page: {str(e)}'.encode('utf-8'))
