# Vercel serverless function for Flask app
# This is the entry point for all requests

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from app import app

# Export the app - Vercel's @vercel/python runtime will handle it automatically
__all__ = ['app']
