"""Vercel serverless function - imports Flask app"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Import Flask app
    from app import app
    print("[API] Flask app imported successfully")
except Exception as e:
    print(f"[API] ERROR importing Flask app: {e}")
    import traceback
    traceback.print_exc()
    # Create minimal error app
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return f'Error loading app: {str(e)}', 500
    
    @app.route('/<path:path>')
    def catch_all(path):
        return f'Error loading app: {str(e)}', 500

# Vercel expects 'app' to be exported
__all__ = ['app']
